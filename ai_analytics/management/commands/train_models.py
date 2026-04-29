from django.core.management.base import BaseCommand
from django.db.models import Q
from ai_analytics.models import StudentSkillAnalysis, CompanySkillDemand
from jobs.models import Application, JobPost
from accounts.models import StudentProfile, CustomUser
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import pickle
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Train ML models for placement prediction using historical data'

    def handle(self, *args, **options):
        self.stdout.write('Starting ML model training...')

        # Collect historical placement data
        applications = Application.objects.select_related('job', 'student', 'student__student_profile').all()

        if not applications.exists():
            self.stdout.write(self.style.WARNING('No application data found. Cannot train models.'))
            return

        # Prepare training data
        data = []
        for app in applications:
            profile = getattr(app.student, 'student_profile', None)
            if not profile:
                continue

            row = {
                'cgpa': profile.cgpa or 0,
                'active_backlogs': profile.active_backlogs,
                'job_min_cgpa': app.job.min_cgpa,
                'job_max_backlogs': app.job.max_backlogs,
                'placed': 1 if app.status == 'Selected' else 0,
                'skills_match': self._calculate_skills_match(profile.skills, app.job.description)
            }
            data.append(row)

        if not data:
            self.stdout.write(self.style.WARNING('No valid training data found.'))
            return

        df = pd.DataFrame(data)

        # Prepare features and target
        X = df[['cgpa', 'active_backlogs', 'job_min_cgpa', 'job_max_backlogs', 'skills_match']]
        y = df['placed']

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate
        accuracy = model.score(X_test, y_test)
        self.stdout.write(f'Model trained with accuracy: {accuracy:.2f}')

        # Save model
        model_path = os.path.join(settings.BASE_DIR, 'ai_models', 'placement_predictor.pkl')
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        with open(model_path, 'wb') as f:
            pickle.dump(model, f)

        self.stdout.write(self.style.SUCCESS(f'Model saved to {model_path}'))

    def _calculate_skills_match(self, student_skills, job_description):
        """Simple skills matching score"""
        if not student_skills or not job_description:
            return 0

        student_skills = set(student_skills.lower().split(','))
        job_text = job_description.lower()

        matches = sum(1 for skill in student_skills if skill.strip() in job_text)
        return matches / len(student_skills) if student_skills else 0
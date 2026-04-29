import os
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from collections import Counter
import re
from django.conf import settings

# Optional imports
try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY', '')
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    openai = None

try:
    from transformers import pipeline
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    pipeline = None
    torch = None

class SkillAnalyzer:
    """AI-powered skill analysis and matching system"""

    def __init__(self):
        # Initialize NLP models lazily
        self.skill_extractor = None
        self._models_loaded = False

        # Common tech skills database
        self.common_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring'],
            'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'jupyter'],
            'soft_skills': ['communication', 'leadership', 'teamwork', 'problem solving']
        }

    def _load_models(self):
        """Lazy load NLP models only when needed"""
        if self._models_loaded:
            return

        if TRANSFORMERS_AVAILABLE:
            try:
                self.skill_extractor = pipeline("ner", model="dslim/bert-base-NER")
                self._models_loaded = True
            except Exception as e:
                print(f"Warning: Could not load NER model: {e}")
                self.skill_extractor = None
        else:
            self.skill_extractor = None

    def extract_skills_from_text(self, text):
        """Extract skills from resume text or job description"""
        if not text:
            return []

        skills_found = []

        # Convert to lowercase for matching
        text_lower = text.lower()

        # Check against common skills database
        for category, skills in self.common_skills.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    skills_found.append(skill.title())

        # Use NLP if available - load models lazily
        self._load_models()
        if self.skill_extractor:
            try:
                entities = self.skill_extractor(text)
                for entity in entities:
                    if entity['entity'] in ['B-PER', 'I-PER']:  # Person entities might be skill names
                        skill = entity['word'].title()
                        if skill not in skills_found:
                            skills_found.append(skill)
            except:
                pass

        return skills_found

    def get_gpt_recommendations(self, student_skills, job_requirements, company_name=""):
        """Get GPT-powered career recommendations"""
        if not OPENAI_AVAILABLE or not openai.api_key:
            return "OpenAI not configured. Please set OPENAI_API_KEY environment variable."

        try:
            client = openai.OpenAI(api_key=openai.api_key)
            prompt = f"""
            Based on the following student skills and job requirements, provide personalized career recommendations:

            Student Skills: {', '.join(student_skills)}
            Job Requirements: {', '.join(job_requirements)}
            Company: {company_name}

            Please provide:
            1. Skill match analysis
            2. Recommended learning path
            3. Career advice
            4. Preparation tips

            Keep response concise and actionable.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error getting GPT recommendations: {str(e)}"

    def calculate_skill_match_score(self, student_skills, job_skills, weights=None):
        """Calculate matching score between student and job skills"""
        if not job_skills:
            return 0.0

        if weights is None:
            weights = {'exact': 1.0, 'partial': 0.5, 'related': 0.2}

        student_skills_lower = [s.lower() for s in student_skills]
        job_skills_lower = [s.lower() for s in job_skills]

        exact_matches = len(set(student_skills_lower) & set(job_skills_lower))
        total_job_skills = len(job_skills)

        if total_job_skills == 0:
            return 0.0

        match_score = (exact_matches / total_job_skills) * 100
        return round(match_score, 2)

    def identify_skill_gaps(self, student_skills, required_skills):
        """Identify skills that student lacks"""
        student_skills_lower = [s.lower() for s in student_skills]
        required_skills_lower = [s.lower() for s in required_skills]

        gaps = []
        for skill in required_skills:
            if skill.lower() not in student_skills_lower:
                gaps.append(skill)

        return gaps

    def recommend_learning_path(self, skill_gaps, timeline_months=6):
        """Generate learning recommendations for skill gaps"""
        recommendations = []

        # Group skills by difficulty
        beginner_skills = []
        intermediate_skills = []
        advanced_skills = []

        for skill in skill_gaps:
            skill_lower = skill.lower()
            if any(s in skill_lower for s in ['html', 'css', 'basic']):
                beginner_skills.append(skill)
            elif any(s in skill_lower for s in ['react', 'django', 'database']):
                intermediate_skills.append(skill)
            else:
                advanced_skills.append(skill)

        # Create learning path
        path = {
            'beginner': beginner_skills,
            'intermediate': intermediate_skills,
            'advanced': advanced_skills,
            'timeline_months': timeline_months,
            'monthly_goals': []
        }

        # Distribute skills across timeline
        all_skills = beginner_skills + intermediate_skills + advanced_skills
        skills_per_month = max(1, len(all_skills) // timeline_months)

        for i in range(timeline_months):
            start_idx = i * skills_per_month
            end_idx = min((i + 1) * skills_per_month, len(all_skills))
            monthly_skills = all_skills[start_idx:end_idx]

            path['monthly_goals'].append({
                'month': i + 1,
                'skills': monthly_skills,
                'resources': self._get_learning_resources(monthly_skills)
            })

        return path

    def _get_learning_resources(self, skills):
        """Get learning resources for skills"""
        resources = {}
        for skill in skills:
            skill_lower = skill.lower()
            if 'python' in skill_lower:
                resources[skill] = ['Codecademy Python', 'freeCodeCamp Python', 'Python.org tutorials']
            elif 'javascript' in skill_lower:
                resources[skill] = ['MDN JavaScript', 'freeCodeCamp JS', 'JavaScript.info']
            elif 'react' in skill_lower:
                resources[skill] = ['React documentation', 'freeCodeCamp React', 'Scrimba React']
            elif 'django' in skill_lower:
                resources[skill] = ['Django documentation', 'Django Girls tutorial', 'MDN Django']
            else:
                resources[skill] = [f'Google "{skill} tutorial"', f'Coursera {skill}', f'Udemy {skill}']

        return resources

class PlacementAnalyzer:
    """AI-powered placement and company analysis"""

    def __init__(self):
        self.skill_analyzer = SkillAnalyzer()

    def analyze_company_skill_demand(self, job_postings):
        """Analyze which skills are most demanded by companies"""
        skill_counts = Counter()
        company_skills = {}

        for job in job_postings:
            skills = self.skill_analyzer.extract_skills_from_text(job.get('description', ''))
            skills.extend(self.skill_analyzer.extract_skills_from_text(job.get('skills_required', '')))

            company = job.get('company', 'Unknown')
            if company not in company_skills:
                company_skills[company] = Counter()

            for skill in skills:
                skill_counts[skill] += 1
                company_skills[company][skill] += 1

        # Calculate demand scores
        total_jobs = len(job_postings)
        skill_demand = {}
        for skill, count in skill_counts.items():
            demand_percentage = (count / total_jobs) * 100
            skill_demand[skill] = {
                'demand_score': round(demand_percentage, 2),
                'frequency': count,
                'companies': [company for company, skills in company_skills.items() if skill in skills]
            }

        return {
            'overall_demand': dict(skill_counts.most_common(20)),
            'skill_demand_analysis': skill_demand,
            'company_focus': dict(company_skills)
        }

    def recommend_students_for_company(self, company_name, job_requirements, students):
        """Recommend students for a specific company based on skills"""
        recommendations = []

        for student in students:
            student_skills = self.skill_analyzer.extract_skills_from_text(
                student.get('skills', '')
            )

            match_score = self.skill_analyzer.calculate_skill_match_score(
                student_skills, job_requirements
            )

            skill_gaps = self.skill_analyzer.identify_skill_gaps(
                student_skills, job_requirements
            )

            if match_score >= 30:  # Only recommend if match is reasonable
                recommendations.append({
                    'student_id': student.get('id'),
                    'student_name': student.get('name', 'Unknown'),
                    'match_score': match_score,
                    'matching_skills': [s for s in student_skills if s.lower() in [j.lower() for j in job_requirements]],
                    'skill_gaps': skill_gaps,
                    'profile': student
                })

        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        return recommendations[:10]  # Top 10 recommendations

    def analyze_placement_trends(self, placement_data):
        """Analyze placement trends and success factors"""
        if not placement_data:
            return {}

        df = pd.DataFrame(placement_data)

        analysis = {
            'total_placements': len(df),
            'placement_rate': 0,
            'top_companies': {},
            'skill_success_factors': {},
            'branch_wise_placement': {},
            'cgpa_distribution': {}
        }

        if 'status' in df.columns:
            placed_count = len(df[df['status'] == 'Selected'])
            analysis['placement_rate'] = round((placed_count / len(df)) * 100, 2)

        if 'company' in df.columns:
            analysis['top_companies'] = df['company'].value_counts().head(10).to_dict()

        if 'branch' in df.columns:
            branch_placement = df.groupby('branch')['status'].apply(
                lambda x: (x == 'Selected').sum()
            ).to_dict()
            analysis['branch_wise_placement'] = branch_placement

        if 'cgpa' in df.columns:
            analysis['cgpa_distribution'] = {
                'average': round(df['cgpa'].mean(), 2),
                'median': round(df['cgpa'].median(), 2),
                'min': df['cgpa'].min(),
                'max': df['cgpa'].max()
            }

        return analysis

class CareerAdvisor:
    """AI career guidance and dream company analysis"""

    def __init__(self):
        self.skill_analyzer = SkillAnalyzer()

    def analyze_dream_company_fit(self, student_profile, dream_company, company_requirements):
        """Analyze how well student fits their dream company"""
        student_skills = self.skill_analyzer.extract_skills_from_text(
            student_profile.get('skills', '')
        )

        current_match = self.skill_analyzer.calculate_skill_match_score(
            student_skills, company_requirements
        )

        skill_gaps = self.skill_analyzer.identify_skill_gaps(
            student_skills, company_requirements
        )

        # Estimate timeline based on skill gaps
        timeline_months = max(3, len(skill_gaps) // 2)  # Rough estimate

        learning_path = self.skill_analyzer.recommend_learning_path(skill_gaps, timeline_months)

        return {
            'current_match_percentage': current_match,
            'required_skills': company_requirements,
            'skill_gaps': skill_gaps,
            'timeline_months': timeline_months,
            'learning_path': learning_path,
            'recommendations': self._generate_improvement_recommendations(skill_gaps, student_profile)
        }

    def _generate_improvement_recommendations(self, skill_gaps, student_profile):
        """Generate personalized improvement recommendations"""
        recommendations = []

        for skill in skill_gaps:
            skill_lower = skill.lower()

            if 'python' in skill_lower:
                recommendations.append({
                    'skill': skill,
                    'priority': 'High',
                    'reason': 'Fundamental programming skill required for most tech roles',
                    'action_items': [
                        'Complete Python basics course',
                        'Build 2-3 small projects',
                        'Practice coding problems on LeetCode'
                    ]
                })
            elif 'database' in skill_lower or 'sql' in skill_lower:
                recommendations.append({
                    'skill': skill,
                    'priority': 'High',
                    'reason': 'Data management is crucial for backend development',
                    'action_items': [
                        'Learn SQL fundamentals',
                        'Practice with MySQL/PostgreSQL',
                        'Work on database design projects'
                    ]
                })
            elif 'javascript' in skill_lower or 'react' in skill_lower:
                recommendations.append({
                    'skill': skill,
                    'priority': 'Medium',
                    'reason': 'Frontend development skills are in high demand',
                    'action_items': [
                        'Master JavaScript fundamentals',
                        'Learn React framework',
                        'Build interactive web applications'
                    ]
                })
            else:
                recommendations.append({
                    'skill': skill,
                    'priority': 'Medium',
                    'reason': 'Valuable skill for career advancement',
                    'action_items': [
                        f'Find online tutorials for {skill}',
                        f'Join {skill} communities',
                        f'Apply {skill} in personal projects'
                    ]
                })

        return recommendations

# Global instances
skill_analyzer = SkillAnalyzer()
placement_analyzer = PlacementAnalyzer()
career_advisor = CareerAdvisor()
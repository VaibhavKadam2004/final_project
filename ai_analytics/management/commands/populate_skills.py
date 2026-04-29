from django.core.management.base import BaseCommand
from ai_analytics.models import SkillMapping

class Command(BaseCommand):
    help = 'Populate initial skill mappings for AI analysis'

    def handle(self, *args, **options):
        skills_data = [
            # Programming Languages
            {'skill_name': 'Python', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 9},
            {'skill_name': 'Java', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'JavaScript', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 9},
            {'skill_name': 'C++', 'category': 'Programming', 'difficulty_level': 'Advanced', 'industry_relevance': 7},
            {'skill_name': 'C#', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'PHP', 'category': 'Programming', 'difficulty_level': 'Beginner', 'industry_relevance': 6},
            {'skill_name': 'Ruby', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 6},
            {'skill_name': 'Go', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Kotlin', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Swift', 'category': 'Programming', 'difficulty_level': 'Intermediate', 'industry_relevance': 6},

            # Web Technologies
            {'skill_name': 'HTML', 'category': 'Web Development', 'difficulty_level': 'Beginner', 'industry_relevance': 8},
            {'skill_name': 'CSS', 'category': 'Web Development', 'difficulty_level': 'Beginner', 'industry_relevance': 8},
            {'skill_name': 'React', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 9},
            {'skill_name': 'Angular', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Vue.js', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Node.js', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Django', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Flask', 'category': 'Web Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Spring', 'category': 'Web Development', 'difficulty_level': 'Advanced', 'industry_relevance': 8},

            # Databases
            {'skill_name': 'MySQL', 'category': 'Database', 'difficulty_level': 'Beginner', 'industry_relevance': 8},
            {'skill_name': 'PostgreSQL', 'category': 'Database', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'MongoDB', 'category': 'Database', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Redis', 'category': 'Database', 'difficulty_level': 'Intermediate', 'industry_relevance': 6},
            {'skill_name': 'Oracle', 'category': 'Database', 'difficulty_level': 'Advanced', 'industry_relevance': 7},
            {'skill_name': 'SQL Server', 'category': 'Database', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'SQLite', 'category': 'Database', 'difficulty_level': 'Beginner', 'industry_relevance': 6},

            # Cloud & DevOps
            {'skill_name': 'AWS', 'category': 'Cloud', 'difficulty_level': 'Intermediate', 'industry_relevance': 9},
            {'skill_name': 'Azure', 'category': 'Cloud', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Google Cloud', 'category': 'Cloud', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Docker', 'category': 'DevOps', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Kubernetes', 'category': 'DevOps', 'difficulty_level': 'Advanced', 'industry_relevance': 8},
            {'skill_name': 'Terraform', 'category': 'DevOps', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Jenkins', 'category': 'DevOps', 'difficulty_level': 'Intermediate', 'industry_relevance': 6},
            {'skill_name': 'Git', 'category': 'DevOps', 'difficulty_level': 'Beginner', 'industry_relevance': 9},

            # Data Science & ML
            {'skill_name': 'Pandas', 'category': 'Data Science', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'NumPy', 'category': 'Data Science', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Scikit-learn', 'category': 'Machine Learning', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'TensorFlow', 'category': 'Machine Learning', 'difficulty_level': 'Advanced', 'industry_relevance': 8},
            {'skill_name': 'PyTorch', 'category': 'Machine Learning', 'difficulty_level': 'Advanced', 'industry_relevance': 8},
            {'skill_name': 'Jupyter', 'category': 'Data Science', 'difficulty_level': 'Beginner', 'industry_relevance': 7},
            {'skill_name': 'Tableau', 'category': 'Data Visualization', 'difficulty_level': 'Beginner', 'industry_relevance': 6},
            {'skill_name': 'Power BI', 'category': 'Data Visualization', 'difficulty_level': 'Beginner', 'industry_relevance': 6},

            # Mobile Development
            {'skill_name': 'Android', 'category': 'Mobile Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'iOS', 'category': 'Mobile Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'React Native', 'category': 'Mobile Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},
            {'skill_name': 'Flutter', 'category': 'Mobile Development', 'difficulty_level': 'Intermediate', 'industry_relevance': 7},

            # Soft Skills
            {'skill_name': 'Communication', 'category': 'Soft Skills', 'difficulty_level': 'Beginner', 'industry_relevance': 9},
            {'skill_name': 'Leadership', 'category': 'Soft Skills', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Teamwork', 'category': 'Soft Skills', 'difficulty_level': 'Beginner', 'industry_relevance': 9},
            {'skill_name': 'Problem Solving', 'category': 'Soft Skills', 'difficulty_level': 'Intermediate', 'industry_relevance': 9},
            {'skill_name': 'Project Management', 'category': 'Soft Skills', 'difficulty_level': 'Intermediate', 'industry_relevance': 8},
            {'skill_name': 'Time Management', 'category': 'Soft Skills', 'difficulty_level': 'Beginner', 'industry_relevance': 8},
        ]

        created_count = 0
        for skill_data in skills_data:
            skill, created = SkillMapping.objects.get_or_create(
                skill_name=skill_data['skill_name'],
                defaults=skill_data
            )
            if created:
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully populated {created_count} skill mappings')
        )
# AI Integration for Internship & Placement Portal

This document describes the AI-powered features integrated into the internship and placement portal for analyzing student skills, company matching, and placement analytics.

## Features Overview

### 1. Student AI Dashboard
**Location:** `/ai/student/dashboard/`

#### Features:
- **Skill Analysis**: Analyzes student's current skills from their profile
- **Company Matching**: Matches students with suitable companies based on job requirements
- **Skill Gap Analysis**: Identifies skills students need to improve
- **Dream Company Analysis**: Analyzes fit for student's dream companies
- **Career Path Suggestions**: AI-powered career recommendations

#### How it works:
1. Student clicks "Analyze My Skills" button
2. AI extracts skills from student's profile text
3. Matches skills against current job postings
4. Identifies skill gaps and provides recommendations
5. Generates career path suggestions

### 2. TPO AI Dashboard
**Location:** `/ai/tpo/dashboard/`

#### Features:
- **Overall Placement Analytics**: Comprehensive placement statistics
- **Skill Demand Analysis**: Identifies most required skills across companies
- **Student Recommendations**: Suggests best students for specific companies
- **Company Skill Analysis**: Analyzes skill requirements for individual companies

#### Analytics Types:
1. **Overall Placement Analysis**
   - Total students, applications, and placements
   - Branch-wise and company-wise placement rates
   - Success metrics and trends

2. **Skill Demand Analysis**
   - Most demanded skills across all job postings
   - Company-specific skill requirements
   - Industry trends and patterns

3. **Student Recommendations**
   - Top matching students for specific companies
   - Skill match percentages
   - Recommended improvements

## Technical Implementation

### Models
- `SkillMapping`: Standardized skill categories and difficulty levels
- `StudentSkillAnalysis`: Stores AI analysis results for students
- `PlacementAnalytics`: Stores TPO analytics data
- `StudentCompanyMatch`: Company matching results
- `DreamCompanyAnalysis`: Dream company fit analysis
- `CompanySkillDemand`: Tracks skill demands by companies

### AI Components

#### SkillAnalyzer Class
- **Skill Extraction**: Uses NLP to extract skills from text
- **Skill Matching**: Cosine similarity for skill-job matching
- **Gap Analysis**: Identifies missing skills
- **Learning Paths**: Generates improvement recommendations

#### PlacementAnalyzer Class
- **Trend Analysis**: Analyzes placement patterns
- **Skill Demand**: Identifies market skill requirements
- **Student Matching**: Recommends students for companies

#### CareerAdvisor Class
- **Dream Company Analysis**: Evaluates fit for target companies
- **Learning Recommendations**: Structured improvement plans
- **Timeline Estimation**: Realistic goal setting

### Dependencies
```
scikit-learn>=1.3.0
pandas>=2.0.0
numpy>=1.24.0
transformers>=4.30.0  # Optional - for advanced NLP
torch>=2.0.0          # Optional - for transformers
openai>=1.0.0         # Optional - for GPT integration
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install scikit-learn pandas numpy transformers torch openai python-dotenv
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Populate Skills Data**:
   ```bash
   python manage.py populate_skills
   ```

4. **Environment Variables** (Optional):
   Create `.env` file for OpenAI API:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage Examples

### Student Skill Analysis
```python
from ai_analytics.utils import skill_analyzer

# Extract skills from text
skills = skill_analyzer.extract_skills_from_text("Python, Django, React developer")

# Calculate match score
match_score = skill_analyzer.calculate_skill_match_score(
    student_skills=['Python', 'Django'],
    job_skills=['Python', 'Django', 'React']
)
```

### Placement Analytics
```python
from ai_analytics.utils import placement_analyzer

# Analyze skill demand
analysis = placement_analyzer.analyze_company_skill_demand(job_postings)

# Get student recommendations
recommendations = placement_analyzer.recommend_students_for_company(
    "Google", ["Python", "Algorithms"], students_data
)
```

## API Endpoints

### Student Endpoints
- `POST /ai/student/analyze-skills/`: Analyze student skills
- `POST /ai/student/analyze-dream-company/`: Analyze dream company fit

### TPO Endpoints
- `GET /ai/tpo/dashboard/`: TPO AI dashboard
- `POST /ai/tpo/generate-analytics/`: Generate placement analytics
- `POST /ai/tpo/company-skill-demand/`: Analyze company skill requirements

## Future Enhancements

1. **Advanced NLP**: Integrate BERT/GPT models for better skill extraction
2. **Predictive Analytics**: Predict placement success based on historical data
3. **Resume Parsing**: Automatic resume analysis and skill extraction
4. **Interview Scheduling**: AI-powered interview time optimization
5. **Personalized Learning**: Adaptive learning path recommendations
6. **Real-time Matching**: Live skill-job matching as students update profiles

## Troubleshooting

### Common Issues:
1. **Missing Dependencies**: Ensure all packages are installed
2. **Empty Analysis**: Check that students have skills entered in profiles
3. **No Job Matches**: Ensure job postings have skill requirements listed

### Performance Optimization:
- Skills analysis cached for 24 hours
- Batch processing for large datasets
- Database indexing on frequently queried fields

## Security Considerations

- All AI analysis respects user privacy
- No personal data sent to external APIs without consent
- Analysis results stored securely in database
- Access controls ensure users only see their own data

## Support

For technical support or feature requests, please contact the development team.
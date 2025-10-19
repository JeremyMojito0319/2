# Environment Configuration for Deployment

## Local Development (.env file)
```env
# GitHub Token for AI features
GITHUB_TOKEN=your_github_token_here

# Supabase Configuration
SUPABASE_URL=https://kgrgsjgcnfxjhnxqtvba.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
DATABASE_URL=postgresql://postgres.kgrgsjgcnfxjhnxqtvba:AqtfCTDoWLRzpQFN@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

## Vercel Environment Variables
When deploying to Vercel, add these environment variables in the Vercel dashboard:

### Required Variables:
1. `DATABASE_URL` - Your Supabase PostgreSQL connection string
2. `GITHUB_TOKEN` - Your GitHub token for AI features  
3. `SUPABASE_URL` - Your Supabase project URL
4. `SUPABASE_KEY` - Your Supabase anon key
5. `SECRET_KEY` - A secure secret key for Flask sessions

### Optional Variables:
1. `FLASK_ENV` - Set to "production" for production deployment

## Security Notes:
- Never commit the .env file to git
- Use different secrets for production vs development
- Rotate keys regularly
- Use Supabase RLS (Row Level Security) for additional data protection
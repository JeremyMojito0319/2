# Supabase Migration - Quick Reference

## ✅ Migration Completed Successfully!

Your note-taking app is now using **Supabase PostgreSQL** instead of SQLite.

---

## 🚀 Starting the Application

```bash
conda activate software
python -m src.main
```

Then open: **http://localhost:5001**

---

## 🔧 Current Setup

- **Database**: Supabase PostgreSQL (Cloud)
- **Connection**: `DATABASE_URL` in `.env`
- **Fallback**: SQLite (if DATABASE_URL is not set)
- **Environment**: conda `software` environment

---

## 📊 What Changed?

### Before (SQLite):
- Local file: `database/app.db`
- Single-user, file-based
- Limited scalability

### After (Supabase):
- Cloud PostgreSQL database
- Multi-user capable
- Highly scalable
- Real-time capabilities
- Automatic backups

---

## 🔄 Database Operations

### View Data in Supabase:
1. Go to https://supabase.com
2. Open your project
3. Navigate to "Table Editor"
4. Select `users` or `notes` table

### Test API:
```powershell
# Get all notes
Invoke-WebRequest http://localhost:5001/api/notes

# Create a note
$note = @{title="Test"; content="Hello Supabase"} | ConvertTo-Json
Invoke-WebRequest http://localhost:5001/api/notes -Method POST -Body $note -ContentType "application/json"
```

---

## 🔄 Switch Between Databases

### Use Supabase (Current):
- Keep `DATABASE_URL` in `.env` file

### Use SQLite (Local Dev):
- Comment out `DATABASE_URL` in `.env`:
  ```
  # DATABASE_URL=postgresql://...
  ```
- Restart the app

---

## 🎯 Features Working

✅ Create/Read/Update/Delete notes
✅ Search notes
✅ Tags support
✅ Event date/time
✅ Drag-drop reordering
✅ AI translation (via GitHub Models)
✅ AI note generation (via GitHub Models)

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | Database configuration |
| `src/main.py` | App entry point with DB config |
| `src/models/note.py` | Note model (PostgreSQL compatible) |
| `src/models/user.py` | User model (PostgreSQL compatible) |
| `scripts/migrate_to_supabase.py` | Migration script |
| `scripts/test_supabase_connection.py` | Connection tester |
| `database/app.db.backup` | SQLite backup |

---

## 🚨 Troubleshooting

### Can't connect to Supabase?
- Check `DATABASE_URL` in `.env`
- Verify Supabase project is active
- Test connection: `python scripts/test_supabase_connection.py`

### App won't start?
- Activate environment: `conda activate software`
- Check dependencies: `pip install -r requirements.txt`
- Check for errors in terminal output

### No data showing?
- Database was empty during migration
- Create new notes in the app
- Check Supabase Table Editor

---

## 📚 Next Steps

1. ✅ **Test the application** - Create, edit, delete notes
2. ✅ **Verify Supabase** - Check data in Supabase dashboard
3. ⏳ **Deploy to Vercel** - Use `vercel --prod` (optional)
4. ⏳ **Add authentication** - Implement Supabase Auth (future)

---

## 💡 Pro Tips

- **Backup**: SQLite backup saved at `database/app.db.backup`
- **Monitoring**: Check Supabase Dashboard → Logs
- **Performance**: Connection pooling enabled automatically
- **Cost**: Supabase free tier includes 500MB database
- **Security**: Use environment variables, never commit `.env`

---

## 🎉 Success!

Your app is now production-ready with a scalable cloud database!

**Application URL**: http://localhost:5001
**Supabase Dashboard**: https://supabase.com/dashboard

---

*For detailed information, see `MIGRATION_SUCCESS.txt`*

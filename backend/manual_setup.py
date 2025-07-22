"""
Manual setup script for Render.com deployment
Run this via Render Shell after deployment
"""
import sys
import os
import time

# Add the project root to the Python path
sys.path.append(os.path.dirname(__file__))

def run_migrations():
    """Run database migrations"""
    import subprocess
    
    print("Running database migrations...")
    try:
        result = subprocess.run(['alembic', 'upgrade', 'head'], 
                              check=True, capture_output=True, text=True)
        print("✅ Migrations completed successfully")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e.stderr}")
        return False

def create_sample_data():
    """Create sample data"""
    print("Creating sample data...")
    try:
        from app.core.database import SessionLocal, engine
        from app.core.security import get_password_hash
        from app.models import *
        from datetime import datetime, timedelta
        import random
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        
        # Create sample users
        users_data = [
            {
                "email": "admin@finansal.com",
                "name": "Sistem Yöneticisi",
                "role": UserRole.ADMIN,
                "password": "admin123"
            },
            {
                "email": "analyst@finansal.com",
                "name": "Risk Analisti",
                "role": UserRole.RISK_ANALYST,
                "password": "analyst123"
            }
        ]
        
        for user_data in users_data:
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing_user:
                user = User(
                    email=user_data["email"],
                    name=user_data["name"],
                    role=user_data["role"],
                    hashed_password=get_password_hash(user_data["password"]),
                    is_active=True
                )
                db.add(user)
        
        db.commit()
        db.close()
        
        print("✅ Sample data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting manual setup for Render.com...")
    
    # Run migrations
    if run_migrations():
        # Create sample data
        create_sample_data()
        print("🎉 Setup completed successfully!")
    else:
        print("❌ Setup failed at migration step")
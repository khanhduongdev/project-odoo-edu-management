# scripts/reset_password.py
from odoo import api, SUPERUSER_ID

def reset_passwords(env):
    # Find all users linked to partners who are Student or Instructor
    users = env['res.users'].search([
        '|', 
        ('partner_id.is_student', '=', True),
        ('partner_id.is_instructor', '=', True),
        ('active', '=', True)
    ])
    
    # Exclude admin and internal superusers to be safe
    users = users.filtered(lambda u: u.id > 5)  # Generally admin is 2
    
    print(f"Found {len(users)} users to reset password...")
    
    count = 0
    for user in users:
        try:
            user.write({'password': '123'})
            print(f"  [OK] Reset password for: {user.name} ({user.login})")
            count += 1
        except Exception as e:
            print(f"  [ERR] Failed for {user.name}: {str(e)}")
            
    print(f"Completed! Reset {count} passwords to '123'.")
    env.cr.commit()

if __name__ == '__main__':
    reset_passwords(env)

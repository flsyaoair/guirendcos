# -*- coding: UTF-8 -*- 
import sys
from src.models import database
from src.models.userprofile import UserProfile,UserStatus
from datetime import datetime

if '-dropcreate' in sys.argv:
    database.drop_database()
    print(u'删除数据库完成')

database.create_database()
print(u'创建数据库完成')

 
session = database.get_session()
admin = UserProfile()
admin.Email = 'admin@admin.com'
admin.Nick = u'admin'
admin.Password = 'admin'
admin.Status = UserStatus.Enabled
admin.IsAdmin = True
admin.RegDate = datetime.now()
session.add(admin)
'''
bug = IssueCategory()
bug.CategoryName = u'Bug'
bug.Status = IssueCategoryStatus.Enabled

issue = IssueCategory()
issue.CategoryName = u'Issue'
issue.Status = IssueCategoryStatus.Enabled

session.add(bug)
session.add(issue)
'''
session.commit()
session.close()


print(u'安装完成')

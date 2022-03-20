from src.services.http.permissions import check_permissions
try:
    check_permissions()
except Exception as e:
    print(e)
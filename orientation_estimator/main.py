import functions_framework
import joblib
from pydantic import BaseModel




@functions_framework.http
def hello(request):
    if request.method == "POST": return "Hello using POST\n"
    if request.method == "GET": return "Wrong method pal...\n"
    return {'name': 'Bernardo', 'age': 26}
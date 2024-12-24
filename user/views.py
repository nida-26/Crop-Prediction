from django.shortcuts import render,redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def blog(request):
    return render(request,"blog.html")

def contact(request):
    return render(request,"contact.html")

def service(request):
    return render(request,"service.html")

def testimonail(request):
    return render(request,"testimonail.html")

def signup(request):
    if request.method =="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        u=request.POST['uname']
        e=request.POST['email']
        p1=request.POST['pass1']
        p2=request.POST['pass2']
        if p1==p2:
            if User.objects.filter(username=u).exists():
                messages.info(request,"Username Available")
                return render(request,"signup.html")
            elif User.objects.filter(email=e).exists():
                messages.info(request,"Email Exists")
                return render(request,"signup.html")
            else:
                #To store value in database
                user=User.objects.create_user(first_name=first, last_name=last, username=u, email=e, password=p1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password Not Matching")
            return render(request,"signup.html")
    else:    
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        u=request.POST['uname']
        p=request.POST['pass1']
        user=auth.authenticate(username=u,password=p)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('/')

def data(request):
    return render(request,"data.html")

def predict(request):
    if request.method == "POST":
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import classification_report, confusion_matrix
        try:
            # Fetching inputs from the form
            n = float(request.POST['nitrogen'])
            p = float(request.POST['phos'])
            k = float(request.POST['potassium'])
            t = float(request.POST['temp'])
            h = float(request.POST['humid'])
            ph = float(request.POST['ph'])
            rain = float(request.POST['rainfall'])

            # Loading dataset
            df = pd.read_csv(r"static/Crop_recommendation.csv")

            # Data preprocessing
            # Drop rows with any missing values
            df.dropna(inplace=True)

            # Define features (X) and target variable (y)
            X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
            y = df["label"]

            # Split data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Feature scaling
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            # Model training
            log = LogisticRegression(max_iter=1000)
            log.fit(X_train_scaled, y_train)

            # Predicting crop for the input values
            input_data = scaler.transform([[n, p, k, t, h, ph, rain]])
            predicted_crop = log.predict(input_data)

            # Evaluation metrics (optional for debugging)
            y_pred = log.predict(X_test_scaled)
            print("Classification Report:")
            print(classification_report(y_test, y_pred))
            print("Confusion Matrix:")
            print(confusion_matrix(y_test, y_pred))

            # Data visualization (optional for debugging)
            sns.violinplot(df["temperature"])
            plt.title("Temperature Distribution")
            plt.show()

            plt.bar(df["N"], df["K"])
            plt.xlabel("Nitrogen")
            plt.ylabel("Potassium")
            plt.title("Nitrogen vs Potassium")
            plt.show()

            return render(request, "predict.html", {
                "n": n, "t": t, "p": p, "k": k, "ph": ph, "h": h, "rain": rain, "crop": predicted_crop[0]
            })
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            messages.error(request, "Error occurred during prediction.")
            return render(request, "predict.html")
    return render(request, "predict.html")

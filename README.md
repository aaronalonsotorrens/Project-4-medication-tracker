
# 💊 Django Medication Tracker with Admin Dashboard & Analytics

This project is a Django-based Medication Tracker designed for users to log their medications and report side effects. It includes an intuitive admin dashboard for high-level insights and basic visualizations using Chart.js.

---

## 🚀 Features

- User authentication (login/register/logout)
- Create, update, and delete medications
- Report side effects per medication
- Side effect category options (dropdown)
- Admin dashboard with:
  - Total medication and side effect counts
  - Top 5 most common side effect categories
  - Bar chart using Chart.js
- Admin access control for dashboard visibility

---

## 🗂️ Project Structure Highlights

```
medication_tracker/
│
├── templates/
│   ├── base.html
│   ├── medication_list.html
│   ├── medication_form.html
│   ├── dashboard.html
│
├── static/
│   └── medication_tracker/css/
│       └── medication_list.css
│
├── models.py
├── views.py
├── forms.py
├── urls.py
└── admin.py
```

---

## 🧠 Models Overview

### Medication
```python
class Medication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.CharField(choices=HEALTH_CATEGORIES)
    ...
```

### SideEffect
```python
class SideEffect(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE, related_name='side_effects')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=SIDE_EFFECT_CATEGORIES)
    description = models.TextField()
    reported_on = models.DateTimeField(auto_now_add=True)
```

---

## 📊 Admin Dashboard (Superusers Only)

### View (`views.py`)
```python
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    total_medications = Medication.objects.count()
    total_side_effects = SideEffect.objects.count()
    most_common_side_effects = SideEffect.objects.values('category')         .annotate(count=models.Count('category'))         .order_by('-count')[:5]

    return render(request, 'medication_tracker/dashboard.html', {
        'total_medications': total_medications,
        'total_side_effects': total_side_effects,
        'most_common_side_effects': most_common_side_effects,
    })
```

### Template (`dashboard.html`)
```html
<canvas id="sideEffectChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const sideEffectData = {
        labels: [{% for effect in most_common_side_effects %}'{{ effect.category }}'{% if not forloop.last %},{% endif %}{% endfor %}],
        datasets: [{
            label: 'Side Effects Count',
            data: [{% for effect in most_common_side_effects %}{{ effect.count }}{% if not forloop.last %},{% endif %}{% endfor %}],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    new Chart(document.getElementById('sideEffectChart'), {
        type: 'bar',
        data: sideEffectData,
        options: { scales: { y: { beginAtZero: true } } }
    });
</script>
```

---

## 🔐 Access Control

- **Dashboard** is only visible to superusers.
- Users can only manage their own medications and side effects.
- Superusers can view all medications in the dashboard.

---

## ✅ How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/medication-tracker.git
   cd medication-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

6. Access the dashboard:
   - Login as a superuser
   - Navigate to `http://localhost:8000/dashboard/`

---

## 🧩 Future Improvements

- Add date filtering to dashboard
- Export insights to CSV
- Introduce charts for medication adherence
- Integrate advanced filtering or user-level analytics

---

## 📸 Screenshot

![Dashboard Preview](your-screenshot-path.png)

---

## 📝 License

MIT License. See `LICENSE` for details.

---

## 🙌 Acknowledgments

Thanks to the Django and Chart.js communities for providing the tools that made this project possible.

from flask import Flask, render_template_string, request, redirect
app = Flask(__name__)
challans = []
next_id = 1

HTML = """
<!DOCTYPE html>
<html>
<head><title>Digital Parking Violation System</title>
<style>
body{font-family:Arial;background:#f2f2f2;padding:20px}
.card{background:white;padding:20px;border-radius:10px;max-width:800px;margin:auto;box-shadow:0 0 10px #ccc}
input,select{width:100%;padding:10px;margin:8px 0;border:1px solid #ccc;border-radius:5px}
.btn{background:#28a745;color:white;padding:12px;border:none;border-radius:5px;width:100%;cursor:pointer;font-size:16px}
.challan{border:1px solid #ddd;padding:15px;border-radius:8px;margin:10px 0}
.pending{color:orange;font-weight:bold}
.paid{color:green;font-weight:bold}
a{color:#007bff;text-decoration:none}
</style></head>
<body><div class="card">
<h2>Digital Parking Violation System</h2>
<p><b>Total Challans:</b> {{total}} | <b>Total Fines:</b> Rs. {{total_fine}} | <b>Pending:</b> {{pending}}</p>
<a href="/">Home</a> | <a href="/report">Report Violation</a> | <a href="/challans">View All Challans</a>
<hr>
<form action="/search" method="GET">
<input type="text" name="q" placeholder="Search by Vehicle Number - Ex: KA01AB1234">
<button class="btn" style="background:#007bff">Search</button>
</form>
<hr>
{% if page == 'home' %}
<h3>Welcome to Parking Violation System</h3>
<p>Report wrong parking, generate challan and pay online.</p>
{% endif %}
{% if page == 'report' %}
<h3>Report Violation</h3>
<form action="/report" method="POST" enctype="multipart/form-data">
<input type="text" name="vehicle" placeholder="Vehicle Number" required>
<input type="text" name="location" placeholder="Location - Ex: MG Road, Bengaluru" required>
<select name="violation"><option>No Parking Zone</option><option>Footpath Parking</option><option>Disabled Spot</option><option>Double Parking</option></select>
<input type="file" name="photo">
<button class="btn">Generate Challan - Rs. 500</button>
</form>
{% endif %}
{% if page == 'list' %}
<h3>All Challans</h3>
{% for c in challans %}
<div class="challan">
<b>{{c.vehicle}}</b> - {{c.location}}<br>
Violation: {{c.violation}} | Fine: Rs. 500<br>
Status: <span class="{{'paid' if c.status=='Paid' else 'pending'}}">{{c.status}}</span><br><br>
{% if c.status == 'Pending' %}
<a href="/pay/{{c.id}}"><button class="btn">Pay Rs. 500</button></a>
{% endif %}
</div>
{% else %}
<p>No challans found.</p>
{% endfor %}
{% endif %}
</div></body></html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, page='home', total=len(challans), total_fine=len(challans)*500, pending=sum(1 for c in challans if c['status']=='Pending'), challans=challans)

@app.route('/report', methods=['GET','POST'])
def report():
    global next_id
    if request.method == 'POST':
        challans.append({'id': next_id, 'vehicle': request.form['vehicle'], 'location': request.form['location'], 'violation': request.form['violation'], 'status': 'Pending'})
        next_id += 1
        return redirect('/challans')
    return render_template_string(HTML, page='report', total=len(challans), total_fine=len(challans)*500, pending=sum(1 for c in challans if c['status']=='Pending'), challans=challans)

@app.route('/challans')
def list_challans():
    return render_template_string(HTML, page='list', total=len(challans), total_fine=len(challans)*500, pending=sum(1 for c in challans if c['status']=='Pending'), challans=challans)

@app.route('/search')
def search():
    q = request.args.get('q','').lower()
    filtered = [c for c in challans if q in c['vehicle'].lower()] if q else challans
    return render_template_string(HTML, page='list', total=len(challans), total_fine=len(challans)*500, pending=sum(1 for c in challans if c['status']=='Pending'), challans=filtered)

@app.route('/pay/<int:id>')
def pay(id):
    for c in challans:
        if c['id'] == id:
            c['status'] = 'Paid'
    return redirect('/challans')

if __name__ == '__main__':
    app.run(debug=True)

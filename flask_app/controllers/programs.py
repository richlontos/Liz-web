from flask_app import app, render_template, request, redirect, session, bcrypt, flash
from flask import Flask, url_for, abort
from flask_app.models.program import Program
import os
import stripe


# TODO ROOT ROUTE


app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51LjRYkCSu5APFJ94So0H8Zxy6uhH1QQL0oaLV3DudB3fcf1WhK3HNjhEXDCW5VVtRf4B1Yw0Rc35ixn7A2fl9eJA00rPXE5ZoA'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51LjRYkCSu5APFJ943ilQXfDnkTbwgA5A3XhLWRRQG73XpBxeMEfrq9nPe1hSmAtIIcHv7gMMnxbDeeKHvCp1dirh00QLtjIDbz'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/programs')
def program_new():

    return render_template("programs.html")


@app.route("/add_program", methods=["POST"])
def add_program():
    if not Program.validate_program(request.form):
        return redirect('/program/new')
    print(request.form)
    Program.save(request.form)
    return redirect('/dashboard')





# TODO LOGOUT
@app.route('/logout')
def logout():

    session.clear()
    return redirect('/')




@app.route('/stripe/pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'beginners',
                },
                'unit_amount': 5000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('beginners_key', _external=True) +
        '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('program_new', _external=True),
    )
       
    return  redirect(session.url, code=303)
    


@app.route('/contact/us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/about/me')
def about_me():
    return render_template('about_me.html')


@app.route('/beginners/course')
def beginners_course():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:

                return redirect('/login/page')
    return render_template('beginners.html')


@app.route('/intermediate/course')
def intermediate_course():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:

                return redirect('/login/page')
    return render_template('intermediate.html')


@app.route('/advance/course')
def advance_course():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:

                return redirect('/login/page')
    return render_template('advance.html')


@app.route('/beginners/exercises')
def beginner_exercises():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:
                return redirect('/login/page')
    return render_template('beginners_exercises.html')


@app.route('/intermediate/exercises')
def intermediate_exercises():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:
                return redirect('/login/page')
    return render_template('intermediate_exercises.html')


@app.route('/advance/exercises')
def advance_exercises():
    if 'user_id' not in session:
        if 'google_id' not in session:
            if 'github_oauth_token' not in session:
                return redirect('/login/page')
    return render_template('advance_exercises.html')


@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)

    payload = request.get_data()
    sig_header = request.environ.get['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_279c4c383158707e22522799668e4a2af1dfe012b8fd3fd71e85dd13d400c2e0'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
    )
    except ValueError as e:
    # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        #invalid signature
        print('INVALID IGNATURE')
        return {}, 400

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']  # contains a stripe.PaymentIntent
        print(session)
    return {} 


@app.route('/beginners/key')
def beginners_key():
    return render_template('beginners_key.html')

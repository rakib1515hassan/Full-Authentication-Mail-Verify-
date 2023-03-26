# def Enter_otp(request):
#     if request.session.has_key('email'):
#         email = request.session['email']
#         user_obj = User.objects.filter(email=email).first()
#         pro_obj = Profile.objects.filter(user=user_obj).first()
#         for u in pro_obj:
#             user_otp = u.otp
#         if request.method == "POST":
#             otp = request.method.get('otp')
#             if not otp:
#                 messages.error(request, "OTP is Required.")
#             elif not user_otp == otp:
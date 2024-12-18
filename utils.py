from kavenegar import *

def send_otp_code(phone_number, code):
	try:
		api = KavenegarAPI("4D5971317A4B5131546D6E59582F5563532B33676A4978517331735137716E4C704F303365504B465A32343D")
		params = {
			"sender": "",
			"receptor": phone_number,
			"message": f"کد تایید عضویت {code} \n ممنون از عضویت شما",
		}
		response = api.sms_send(params)
		print(response)
	except APIException as e:
		print(e)
	except HTTPException as e:
		print(e)
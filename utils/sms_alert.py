def send_sms_alert(

    phone,

    district,

    risk_level

):

    print("""

====================

SMS SENT

Phone:

{}

District:

{}

Risk:

{}

====================

""".format(

        phone,

        district,

        risk_level

    ))

    return True
# from backend.app.providers.email_provider import EmailProvider
# from backend.app.providers.whatsapp_provider import WhatsAppProvider
# from backend.app.providers.call_provider import CallProvider
# from backend.app.providers.reminder_provider import ReminderProvider


# email_provider = EmailProvider()
# whatsapp_provider = WhatsAppProvider()
# call_provider = CallProvider()
# reminder_provider = ReminderProvider()


# def execute_trigger(follow_up) -> bool:

#     if follow_up.type == "email":

#         return email_provider.send(
#             to=follow_up.client.email,
#             subject="Follow-up Reminder",
#             message=follow_up.message,
#         )

#     elif follow_up.type == "whatsapp":

#         return whatsapp_provider.send(
#             phone=follow_up.client.phone,
#             message=follow_up.message,
#         )

#     elif follow_up.type == "call":

#         return call_provider.call(
#             phone=follow_up.client.phone,
#         )

#     elif follow_up.type == "reminder":

#         return reminder_provider.remind(
#             message=follow_up.message,
#         )

#     else:

#         raise ValueError(
#             f"Unsupported follow-up type: {follow_up.type}"
#         )


from backend.app.providers.email_provider import EmailProvider
from backend.app.providers.whatsapp_provider import WhatsAppProvider
from backend.app.providers.call_provider import CallProvider
from backend.app.providers.reminder_provider import ReminderProvider


email_provider = EmailProvider()
whatsapp_provider = WhatsAppProvider()
call_provider = CallProvider()
reminder_provider = ReminderProvider()


def execute_trigger(follow_up):
    if follow_up.type == "email":
        return email_provider.send(
            to=follow_up.client.email,
            subject="Follow-up Reminder",
            message=follow_up.notes,
        )

    elif follow_up.type == "whatsapp":
        return whatsapp_provider.send(
            phone=follow_up.client.phone,
            message=follow_up.notes,
        )

    elif follow_up.type == "call":
        return call_provider.call(
            phone=follow_up.client.phone
        )

    elif follow_up.type == "reminder":
        return reminder_provider.remind(
            message=follow_up.notes
        )

    else:
        raise ValueError(
            f"Unsupported follow-up type: {follow_up.type}"
        )
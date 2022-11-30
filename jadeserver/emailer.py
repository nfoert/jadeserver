import os
import django

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jadeserver.settings")
    django.setup()

    from jadeCore.models import Account
    from trycourier import Courier
    client = Courier(auth_token="pk_prod_78G758D0ZZ4VPQJN79MDWTYTHESR")

    allAccounts = Account.objects.all()
    for i in range(len(allAccounts)):
        print(f"Sending email with username: '{allAccounts[i].userName}' and email '{allAccounts[i].email}'")
        resp = client.send(
            event="V7SRR5CC8Z4VP3MXAXXBZTV20N3G",
            recipient="Hello test",
            profile={
                "email": allAccounts[i].email,
            },
            data={
            "recipientName": allAccounts[i].userName
            }
        )

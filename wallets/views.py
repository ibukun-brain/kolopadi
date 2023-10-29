import json

from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from kolopadi.utils.env_variable import get_env_variable
from wallets.models import Transaction


@transaction.atomic
@require_POST
@csrf_exempt
def FlutterwaveWebhookView(request):
    secret_hash = get_env_variable("FLUTTERWAVE_SECRET_HASH")
    signature = request.headers.get("Verif-Hash")
    if signature is None or (signature != secret_hash):
        # This request isn't from Flutterwave; discard
        return HttpResponse(status=401)
    payload = json.loads(request.body)
    if payload["event.type"] == "Transfer":
        data = payload.get("data")
        transfer_id = data["id"]
        reference_id = f"FLWRVCNF{transfer_id}"
        transactions = None

        try:
            transactions = Transaction.objects.select_related("wallet").filter(
                reference=reference_id,
                type="D",
                amount=data["amount"],
            )
        except Transaction.DoesNotExist:
            pass
        if transactions.exists():
            transactions = transactions.first()
            transactions.external_recipient = data["fullname"]
            transactions.external_recipient_account_no = data["account_number"]
            transactions.external_recipient_bank = data["bank_name"]
            transactions.transfer_status = data["status"]
            transactions.save()
            return HttpResponse(status=200)
    return HttpResponse(status=200)

def from_payload_to_user_info(payload):
    user_info = {
        "id": payload["user_id"],
        'username': payload['username'],
    }
    return user_info


def jwt_response_payload_handler(token, user, request):
    response_data = {
        "token": token,
        "user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    if "from_admin" in request.data:
        response_data["is_staff"] = user.is_staff
        response_data["is_superuser"] = user.is_superuser
    return response_data

def user_serialiser(user)->dict:
    return{
        "_id":str(user["name"]),
        "name":user["name"],
        "email":user["email"],
        "password":user["password"],
        "phone":user["phone"],
    }


def user_list_serialiser (users)->list:
    return[ user_serialiser(user) for user in users]

from django.dispatch import receiver

# from .models import UserProfile
from django.contrib.auth.models import User
from metabase.models import MetabaseUserData
from users.models import CustomUser
from pprint import pprint

from metabase.connector.metabase_conn import MetabaseClient


def create_metabase_user(profile: CustomUser, user: User):
    metabase_client = MetabaseClient()
    group_name = f"{profile.username}_group"
    metabase_group = metabase_client.create_group(name=group_name)
    pprint(metabase_group)

    metabase_user = metabase_client.create_user(
        email=user.email, fname=profile.username, lname=user.last_name
    )
    pprint(metabase_user)

    metabase_relation = metabase_client.add_user_to_group(
        group_id=metabase_group["id"],
        user_id=metabase_user["id"],
    )
    pprint(metabase_relation)

    metabase_user_data = MetabaseUserData(
        user=user,
        metabase_id=metabase_user["id"],
        metabase_group_id=metabase_group["id"],
    )
    metabase_user_data.save()


# @receiver(user_signed_up)
# def save_extra_data(request, user: User, **kwargs):
#     social_account = SocialAccount.objects.filter(user=user).first()
#     if social_account:
#         extra_data = social_account.extra_data

#         login = extra_data.get("login")
#         name = extra_data.get("name")
#         bio = extra_data.get("bio")
#         company_name = extra_data.get("company")
#         email = extra_data.get("email")
#         location = extra_data.get("location")
#         avatar_url = extra_data.get("avatar_url")
#         user_url = extra_data.get("url")
#         github_id = extra_data.get("id")

#         profile, created = UserProfile.objects.get_or_create(user=user)
#         profile.login = login
#         profile.name = name
#         profile.bio = bio
#         profile.company_name = company_name
#         profile.email = email
#         profile.location = location
#         profile.avatar_url = avatar_url
#         profile.user_url = user_url
#         profile.github_id = github_id
#         profile.save()

#         try:
#             create_metabase_user(profile, user)
#         except Exception as e:
#             pprint(e)

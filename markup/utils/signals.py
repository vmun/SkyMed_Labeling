import logging

from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from markup.utils.ChoiceFields import *
from markup.models import *
from markup.utils.document_upload import task_delete_path

user_logger = logging.getLogger('user_logger')
actions_logger = logging.getLogger('actions_logger')


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        user_logger.info(f"{instance} registered!\n")
    if instance:
        if instance.is_superuser:
            imagePacks = ImagePack.objects.all()
            for pack in imagePacks:
                AllowedImagePack.objects.create(imagePack=pack, user=instance)


@receiver(post_save, sender=Folder)
def folder_created(sender, instance, created, **kwargs):
    if created:
        actions_logger.info(f"Folder {instance} created!\n")


@receiver(post_save, sender=ImagePack)
def imagePack_created(sender, instance, created, **kwargs):
    if created:
        actions_logger.info(f"ImagePack {instance} created!\n")
        superusers = MainUser.objects.filter(is_superuser=True)
        for superuser in superusers:
            AllowedImagePack.objects.create(imagePack=instance, user=superuser)


@receiver(post_save, sender=AllowedImagePack)
def permission_created(sender, instance, created, **kwargs):
    if created:
        actions_logger.info(f"{instance.user} was given access to {instance.imagePack}!\n")


@receiver(post_delete, sender=Image)
def document_deleted(sender, instance, **kwargs):
    print('started deleting doc')
    if instance:
        task_delete_path(document=instance)
        print('deleted')

# -*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(days=1)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute) #created__gte, objects.filter的用法
    if target:
        target_ct = ContentType.objects.get_for_model(target) #objects.get_for_model的用法
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)

    if not similar_actions:
        # 没有发现similar_action
        if target:
            action = Action(user=user, verb=verb, target=target,target_text=target.text)
        else:
            action = Action(user=user, verb=verb)
        action.save()
        return True
    return False #存在similar_actions

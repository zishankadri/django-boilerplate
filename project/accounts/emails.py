from .utils import send_email

def send_verification_email(email, auth_token, domain_name):
    subject = "Confirmation de votre inscription sur AutoPrep"
    # Objet: Confirmation de votre inscription sur AutoPrep
    # Cher/Chère [user name],
    message = f'''
Nous sommes ravis de vous accueillir sur AutoPrep, votre assistant pédagogique en ligne ! Votre inscription est désormais presque complète.

Afin de confirmer votre adresse e-mail et de finaliser votre inscription, veuillez cliquer sur le lien ci-dessous :

{domain_name}/accounts/verify_email/{auth_token}/

Une fois cette étape accomplie, vous aurez accès à toutes les fonctionnalités incroyables d'AutoPrep, y compris la création de cours, la génération de contrôles et la correction automatique. Nous sommes convaincus que notre plateforme vous aidera à optimiser votre préparation pédagogique et à offrir une expérience d'apprentissage enrichissante à vos élèves.

N'hésitez pas à nous contacter si vous avez des questions ou des préoccupations. Notre équipe est là pour vous aider à tirer le meilleur parti de votre expérience sur AutoPrep.

Nous avons hâte de vous voir en action sur la plateforme !

Cordialement,

L'équipe AutoPrep
'''
    send_email(subject=subject, message=message, email=email)


def send_change_password_email(email, auth_token, domain_name):
    subject = "Réinitialisation de votre mot de passe AutoPrep"
    message = f'''
Nous avons remarqué que vous avez demandé une réinitialisation de votre mot de passe pour votre compte AutoPrep. Ne vous inquiétez pas, nous sommes là pour vous aider à récupérer l'accès à votre compte en un rien de temps !

Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien ci-dessous :

{domain_name}/accounts/change_password/{email}/{auth_token}/

Une fois que vous avez cliqué sur le lien, vous serez redirigé vers une page où vous pourrez choisir un nouveau mot de passe sécurisé.

Si vous n'avez pas demandé cette réinitialisation ou si vous rencontrez des problèmes pour accéder à votre compte, veuillez nous contacter immédiatement pour que nous puissions vous aider.

Nous vous remercions de votre confiance en AutoPrep pour vos besoins pédagogiques. N'hésitez pas à nous contacter si vous avez d'autres questions ou préoccupations.

Cordialement,

L'équipe AutoPrep
'''

    send_email(subject=subject, message=message, email=email)




# def send_verification_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Verify your email address"
#     message = f"Verify your email for Algostockz by clicking :- {domain_name}/accounts/verify/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)

# def changing_email_verificatin(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Verify your email address"
#     message = f"Verify your email for Algostockz by clicking :- {domain_name}/accounts/change_email_final/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)


# def send_change_password_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Change Password"
#     message = f"Change password for Algostockz by clicking :- {domain_name}/accounts/change_password/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)


# def send_change_email_email(email, auth_token):
#     email_from = settings.EMAIL_HOST_USER

#     subject = "Change Email"
#     message = f"Change Email for Algostockz by clicking :- {domain_name}/accounts/change_email/{auth_token}/"
#     recipient_list = [email, ]
    
#     send_mail(subject, message, email_from, recipient_list, fail_silently = False)


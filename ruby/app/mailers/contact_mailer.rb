class ContactMailer < ApplicationMailer

  # Subject can be set in your I18n file at config/locales/en.yml
  # with the following lookup:
  #
  #   en.contact_mailer.comment.subject
  #
  def comment(name, email, comment)
    @name = name
    @email = email
    @comment = comment

    mail to: "philippbraun95@aol.com", subject: "Wenti - Contact"
  end
end

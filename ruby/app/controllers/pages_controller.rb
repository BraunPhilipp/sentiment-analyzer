class PagesController < ApplicationController
  skip_before_filter :verify_authenticity_token

  def home
  end

  def search
  end

  def contact
  end

  def privacy
  end

  def legal
  end

  def sender

    unless params[:name].blank? && params[:email].blank? && params[:comment].blank?
      ContactMailer.comment(params[:name], params[:email], params[:comment]).deliver
      render status: 200, json: {
        message: "Successfully sent Mail"
      }.to_json and return
    end

    render status: 422, json: {
      message: "Could not send Mail"
    }.to_json and return

  end

end

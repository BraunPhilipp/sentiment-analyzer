class Api::TweetVolumesController < Api::ApiController

  before_filter :admin_access

  def index
    render json: TweetVolume.all
  end

  def create
    list = TweetVolume.new(json_params)

    if !list.save
      render status: 422, json: {
        message: "Could not add a Tweet Volume!",
        tweet: list
      }.to_json and return
    end

    render status: 200, json: {
      message: "Tweet Volume was added to Database!"
    }.to_json
  end

  private
    def json_params
      params.require(:tweet_volume).permit(:tracker_id, :date, :volume)
    end

    def admin_access
      head :unauthorized unless Rails.application.secrets.api_key == params[:api_key]
    end

end

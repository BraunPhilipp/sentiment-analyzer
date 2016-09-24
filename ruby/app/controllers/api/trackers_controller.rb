class Api::TrackersController < Api::ApiController

  before_filter :admin_access, :except => [:index, :show]
  before_filter :user_access, :only => [:index, :show]

  def index
    render json: Tracker.all
  end

  def show
    list = Tracker.find(params[:id])
    render json: list
  end

  def search
    list = Tracker.where(:keyword => params[:q])
    if params.has_key?(:sort)
      list = list.order(params[:sort] => :asc)
    end
    if params.has_key?(:limit)
      list = list.limit(params[:limit])
    end
    render json: list
  end

  def next
    list = Tracker.all.order(:updated_at => :asc).limit(1)
    render json: list
  end

  # curl -i -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"keyword":"hillary+clinton"}' http://localhost:3000/api/trackers

  def create
    list = Tracker.new(list_params)
    if Tracker.where(:keyword => params[:keyword]).empty?
      list.save
      render status: 200, json: {
        message: "Successfully created Keyword",
        tracker: list
      }.to_json
    else
      render status: 422, json: {
        message: "Keyword cannot be blank or duplicate",
        errors: list.errors
      }.to_json
    end
  end

  # curl -i -H "Accept: application/json" -H "Content-type: application/json" -X PUT -d "{\"min_id\":\"10\"}" http://localhost:3000/api/trackers/3.json

  def update
    list = Tracker.find(params[:id])

    if(params[:min_id] < list.min_id && params[:min_id] != 0 || list.min_id == 0)
      list.update(:min_id => params[:min_id])
    end

    if(params[:max_id] > list.max_id && params[:max_id] != 0 || list.max_id == 0)
      list.update(:max_id => params[:max_id])
    end

    list.update(:volume => list.volume + params[:volume])

    render status: 200, json: {
      message: "Succesfully updated Keyword",
      tracker: list
    }.to_json
  end

  # curl -i -H "Accept: application/json" -H "Content-type: application/json" -X DELETE http://localhost:3000/api/trackers/4.json

  def delete
    if Tracker.exists?(:keyword => params[:keyword])
      list = Tracker.where(:keyword => params[:keyword])
      list.destroy_all
      render status: 200, json: {
        message: "Successfully destroyed Keyword"
      }.to_json
    else
      render status: 422, json: {
        message: "Failed to delete Keyword"
      }.to_json
    end
  end

  private
    def list_params
      params.require(:tracker).permit(:keyword, :volume, :min_id, :max_id)
    end

    def admin_access
      head :unauthorized unless Rails.application.secrets.api_key == params[:api_key]
    end

    def user_access
      # Users will be added lateron including signup form
      head :unauthorized unless "12345" == params[:api_key] || Rails.application.secrets.api_key == params[:api_key]
    end

end

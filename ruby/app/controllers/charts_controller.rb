class ChartsController < ApplicationController

  include ChartsHelper

  def index
    get_data
  end

  def data
    get_data

    if params[:format] == 'json'
      render json: @data
    else
      # Generate CSV
      csv = ""
      @data.each do |i|
        csv += i[:date].strftime('%Y-%m-%d') + ","
        i[:val].each do |j|
          csv += j.to_s + ","
        end
        csv += "\n"
      end
      # Output CSV
      render plain: csv, :content_type => "text/csv"
    end

  end

end

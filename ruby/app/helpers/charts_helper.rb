module ChartsHelper
  def current_keywords
    Tracker.all
  end

  def get_data
    @query = params[:q].split(/,/)

    @data ||= []

    # Add Keyword Data
    @query.each do |keyword|
      list = keyword.split(/:/)

      key = Tracker.where(:keyword => list[1]).first
      sen = TweetSentiment.where(:tracker_id => key.id)

      # Add Sentiment to val
      new_data ||= []
      unless sen.empty?
        sen.each do |item|
          new_data << {:date => item.date, :val => [item.sentiment]}
        end
      end

      new_data.delete_if { |h| h[:val] == [0] }

      if @data.empty?
        @data = new_data
      else
        # Add new data to array
        @data.each do |i|
          new_data.each do |j|
            if i[:date] == j[:date]
              i[:val] << j[:val].first
            end
          end
        end

        # Drop not filled fields
        @data.delete_if { |h| h[:val].length == @query.index(keyword) }
      end
    end

    # Each data point
    @data.each_index do |i|
      # Each value
      @data[i][:val].each_index do |j|
        if @query[j].split(/:/).first.split(/_/).first == 'cum'
          if i > 0
            @data[i][:val][j] = @data[i-1][:val][j] * (1 + ((@data[i][:val][j].to_f - 500) / 100000))
            @data[i][:val][j] = @data[i][:val][j].round
          else
            @data[i][:val][j] = 1000
          end
        end
      end
    end
    
  end

end

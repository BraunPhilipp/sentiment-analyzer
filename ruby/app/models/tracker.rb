class Tracker < ActiveRecord::Base
  validates :keyword, presence: true, length: { minimum: 3 }
end

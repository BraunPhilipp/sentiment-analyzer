class CreateReviews < ActiveRecord::Migration
  def change
    create_table :reviews do |t|
      t.text :text
      t.string :category
      t.integer :score

      t.timestamps null: false
    end
  end
end

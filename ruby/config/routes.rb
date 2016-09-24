Rails.application.routes.draw do

  namespace :api do
    get 'trackers/search' => 'trackers#search'
    get 'trackers/next' => 'trackers#next'
    put 'trackers' => 'trackers#update'
    delete 'trackers' => 'trackers#delete'
    resources :trackers

    get 'reviews/search' => 'reviews#search'
    resources :reviews

    get 'tweet_datums/search' => 'tweet_datums#search'
    resources :tweet_datums

    resources :tweet_volumes

    delete 'tweet_sentiments' => 'tweet_sentiments#delete'
    resources :tweet_sentiments
  end

  root 'pages#home'

  get 'home' => 'pages#home'
  get 'search' => 'pages#search'
  get 'contact' => 'pages#contact'
  post 'sender' => 'pages#sender'
  get 'privacy' => 'pages#privacy'
  get 'legal' => 'pages#legal'

  get 'chart' => 'charts#index'
  get 'data' => 'charts#data'

  # The priority is based upon order of creation: first created -> highest priority.
  # See how all your routes lay out with "rake routes".

  # You can have the root of your site routed with "root"
  # root 'welcome#index'

  # Example of regular route:
  #   get 'products/:id' => 'catalog#view'

  # Example of named route that can be invoked with purchase_url(id: product.id)
  #   get 'products/:id/purchase' => 'catalog#purchase', as: :purchase

  # Example resource route (maps HTTP verbs to controller actions automatically):
  #   resources :products

  # Example resource route with options:
  #   resources :products do
  #     member do
  #       get 'short'
  #       post 'toggle'
  #     end
  #
  #     collection do
  #       get 'sold'
  #     end
  #   end

  # Example resource route with sub-resources:
  #   resources :products do
  #     resources :comments, :sales
  #     resource :seller
  #   end

  # Example resource route with more complex sub-resources:
  #   resources :products do
  #     resources :comments
  #     resources :sales do
  #       get 'recent', on: :collection
  #     end
  #   end

  # Example resource route with concerns:
  #   concern :toggleable do
  #     post 'toggle'
  #   end
  #   resources :posts, concerns: :toggleable
  #   resources :photos, concerns: :toggleable

  # Example resource route within a namespace:
  #   namespace :admin do
  #     # Directs /admin/products/* to Admin::ProductsController
  #     # (app/controllers/admin/products_controller.rb)
  #     resources :products
  #   end
end

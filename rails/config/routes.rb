Rails.application.routes.draw do
  get 'home/index'
  get 'intuitive-brief', to: 'home#brief'
  root :to => "home#index"

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end

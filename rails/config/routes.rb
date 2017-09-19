Rails.application.routes.draw do
  get 'home/index'
  get 'intuitive-brief', to: 'home#brief'
  get 'hello', to: 'home#hello'
  get 'search', to: 'home#search'
  get 'tags', to: 'home#tags'
  get 'zoom-in', to: 'home#zoom', as: :zoom
  get 'summary', to: 'home#summary'
  root :to => "home#index"

  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end

class HomeController < ApplicationController
  def index ; end
  def brief ; end
  def hello ; end
  def search
    if params[:boton] == "searched"
      data = session[:data] || {}
      data[:category] = params[:category]
      data[:industry] = params[:industry]
      session[:data] = data
    end
  end
end

require 'faker'
class Interaction

  def self.new_place_holder_user(session_id:)
    begin
      user = User.find_by(session_id: session_id)
      return user
    rescue Mongoid::Errors::DocumentNotFound
      user = User.new
    end    

    user.full_name =  Faker::Name.name
    user.user_type = User::UNDEFINED_TYPE
    user.session_id = session_id
    tries = 50

    while(!user.valid? && tries > 0) do
      user.email = Faker::Internet.email
      tries -= 1
    end

    return nil if !user.save
    return user
  end

  def self.retrieve_or_create_user(full_name:, email:, user:)
    full_name = full_name.strip
    email = email.strip

    return nil if !user
    begin
      old_user = User.find_by(email: email)
    rescue Mongoid::Errors::DocumentNotFound
      old_user = nil
    end

    if old_user
      old_user.full_name = full_name
      old_user.email = email

      return old_user
    end

    user.full_name = full_name
    user.email = email

    return user
  end

  def self.current_intention(user:)
    intentions = Intention.where(user: user, status: Intention::PENDING_STATUS)
    raise "ERROR to many tries" if intentions.count > 1

    if intentions.empty?
      intention = Intention.new(user: user)
      intention.save!
      return intention
    end

    return intentions.last
  end
end
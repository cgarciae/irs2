require "rails_helper"

RSpec.describe Interaction, :type => :model do
  describe ".new_place_holder_user" do

    it "creates a new user" do
      user = Interaction.new_place_holder_user(session_id: "1")
      old_full_name = user.full_name
      old_email = user.email

      params = {
        full_name: "pep perez",
        email: "pep@example.com",
        user: user
      }

      user_ = Interaction.retrieve_or_create_user(params)

      expect(user.full_name).not_to eq(old_full_name)
      expect(user.email).not_to eq(old_email)
      expect(user).to be_valid
    end

    it "returns existing user" do
      user = Interaction.new_place_holder_user(session_id: "1")
      user.save!

      user_ = Interaction.new_place_holder_user(session_id: "2")
      new_email = user_.email
      user_.email = user.email
      params = {
        full_name: "pep perez",
        email: user_.email,
        user: user_
      }

      user__ = Interaction.retrieve_or_create_user(params)

      expect(user.full_name).not_to eq("pep perez")
      expect(user__.email).not_to eq(new_email)
      expect(user__.email).to eq(user.email)
      expect(user__.id.to_s).not_to eq(user_.id.to_s)
      expect(user__.id.to_s).to eq(user.id.to_s)
      expect(user__).to be_valid
    end

  end
end
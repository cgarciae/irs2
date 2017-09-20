class Tags

SITUATIONAL_ARCHETYPES = {
  "The Quest" => %W(hero accomplish bring fertility
  wastelsearch talisman restore peace order normalcy),
  "The Task" => %W(nearly superhuman feat perform
order accomplish quest),
  "The Journey" => %W(journey sends search truth help save kingdom),
  "The Initiation" => %W(adolescent maturity new
awareness problems ),
  "The Ritual" => %W(actual ceremonies initiate experiences will
mark rite passage another state clear sign
character's role society),
  "The Fall" => %W(descent higher lower state
 punishment transgression involves loss innocence),
  "Death Rebirth" => %W(motif
grows parallel cycle nature
cycle life morning springtime represent birth
youth rebirth evening winter old age death),
  "Battle between Good
Evil" => %W(battle primal forces Mankind eternal optimism continual portrayal
triumphing evil odds),
  "The Unhealable Wound" => %W(physical psychological wound 
fully healed wound symbolizes loss innocence)
}
  
CHARACTER_ARCHETYPES = {
  "The Hero" => %W(protagonist life series 'well-
marked' adventures circumstances birth
unusual raised guardian
leave kingdom reaching
manhood Characterized courage strength
honor endure hardship even risk life
good Leaves familiar enter
unfamiliar challenging world),
  "Young Man the Provinces" => %W(home heritage stranger new problems
solutions),
  "The Initiates" => %W(Initiates young heroes heroines must go
through training ceremony
undertaking quest),
  "Mentor" => %W(mentor wiser teacher initiates
 serves father mother figure  gives
hero gifts weapons food magic information
serves role conscience),
  "Mentor - Pupil
Relationship" => %W(relationship Mentor teaches
necessary skills surviving quest),
  "The Threshold
Guardian" => %W(tests hero courage worthiness begin
journey),
  "Father - Son Conflict" => %W(relationship tension built due
separation childhood source),
  "Hunting Group of
Companions" => %W(loyal companions willing face hardship
ordeal order stay together),
  "Loyal Retainers" => %W(duty reflect nobility power),
  "Friendly Beast" => %W(animal companion showing nature
side hero),
  "The Shadow" => %W(worthy opponent hero must struggle
fight Must destroyed neutralized
Psychologically represent darker side
psyche),
  "The Devil Figure" => %W(This character evil incarnate),
  "The Evil Figure with
Ultimately Good Heart" => %W(devil figure potential good
person saved love hero),
  "The Creature of
Nightmare" => %W(monster summoned deepest darkest
part human psyche threaten lives
perversion desecration
human body),
  "The Scapegoat" => %W(animal human death public ceremony expiates taint sin community powerful death life),
  "The Outcast" => %W(character banished social group real imagined crime against fellow man destined wander form place),
  "The Platonic Ideal" => %W(woman source inspiration hero intellectual physical attraction),
  "Damsel Distress" => %W(vulnerable woman rescued the trap ensnare unsuspecting hero),
  "The Earth Mother" => %W(Symbolic fruition abundance fertility
traditionally spiritual emotional
nourishment contact depicted earth colors
hips childbearing capacities),
  "The Temptress Black
Goddess" => %W(sensuous beauty protagonist physically attracted
ultimately downfall
witch vampire),
  "White Goddess" => %W(beautiful maiden blond make
ideal religious intellectual overtones),
  "The Unfaithful Wife" => %W(dull distant
 attracted virile interesting),
  "Star-Crossed Lovers" => %W(engaged love affair fated
tragically disapproval society friends family tragic situation)
}

MIND_MARKS = {
  "Dream" => %W(dream),
  "Niche" => %W(niche),
  "Land" => %W(land),
  "Magic" => %W(magic),
  "Question" => %W(question),
  "Trust" => %W(trust),
  "UnMarked" => %W(unmarked),
  "Service" => %W(service),
  "Category" => %W(category)
}

BRAND_VALUES = {
  "Quality" => %W(quality customers confident refund reliability),
  "Value" => %W(value uniqueness innovation),
  "Fun" => %W(happiness perspective fashion),
  "Trust" => %W(brand trust loyal promise),
  "Passion" => %W(passion products boldness)
}

  def self.all
    [
      SITUATIONAL_ARCHETYPES.values.sample(8) +
      CHARACTER_ARCHETYPES.values.sample(8) +
      MIND_MARKS.values +
      BRAND_VALUES.values
    ].flatten.map{|d| d.downcase}
  end
end
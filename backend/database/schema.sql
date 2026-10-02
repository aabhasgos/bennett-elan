-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- PROFILES (Extended from auth.users)
CREATE TABLE public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    first_name TEXT NOT NULL,
    age INTEGER CHECK (age >= 18),
    course TEXT,
    year TEXT,
    bio TEXT, -- Optional, mostly prompts are used
    instagram_handle TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- PREFERENCES (What they are looking for)
CREATE TABLE public.preferences (
    profile_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE PRIMARY KEY,
    intentions TEXT[] DEFAULT '{}', -- 'date', 'dance_partner', 'friends', 'group'
    looking_for_gender TEXT[] DEFAULT '{}', -- 'male', 'female', 'other'
    min_age INTEGER DEFAULT 18,
    max_age INTEGER DEFAULT 25,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- INTERESTS (Tags like Music, Basketball)
CREATE TABLE public.interests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL
);

-- PROFILE_INTERESTS (Many-to-Many)
CREATE TABLE public.profile_interests (
    profile_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    interest_id UUID REFERENCES public.interests(id) ON DELETE CASCADE,
    PRIMARY KEY (profile_id, interest_id)
);

-- PROMPTS (Configurable by admin)
CREATE TABLE public.prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category TEXT NOT NULL, -- 'Ball Night', 'Personality', 'Fun'
    question TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- PROFILE_PROMPTS (Answers)
CREATE TABLE public.profile_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    prompt_id UUID REFERENCES public.prompts(id) ON DELETE CASCADE,
    answer TEXT NOT NULL,
    position INTEGER DEFAULT 0, -- Order on profile
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (profile_id, prompt_id)
);

-- SWIPES (Like/Pass)
CREATE TABLE public.swipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    swiper_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    swipee_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    action TEXT CHECK (action IN ('like', 'pass')) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE (swiper_id, swipee_id)
);

-- MATCHES (When A likes B and B likes A)
CREATE TABLE public.matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user1_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    user2_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

CREATE UNIQUE INDEX unique_match_pair ON public.matches (
    LEAST(user1_id, user2_id), 
    GREATEST(user1_id, user2_id)
);

-- MESSAGES (Chat after match)
CREATE TABLE public.messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    match_id UUID REFERENCES public.matches(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- EVENT_PLANS (Plan Your Night together)
CREATE TABLE public.event_plans (
    match_id UUID REFERENCES public.matches(id) ON DELETE CASCADE PRIMARY KEY,
    outfit_status TEXT, -- 'decided', 'figuring_out', 'need_inspiration'
    arrival_time TEXT, -- 'early', '8pm', 'later'
    meet_location TEXT, -- 'campus', 'friends', 'event'
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- RSVPS
CREATE TABLE public.rsvps (
    profile_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE PRIMARY KEY,
    status TEXT CHECK (status IN ('attending', 'not_sure', 'not_attending')) NOT NULL,
    digital_pass_qr TEXT, -- Can be generated later
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Row Level Security (RLS) setup - Basic rules to secure data
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.swipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;

-- Allow users to read their own profile and profiles of matches
CREATE POLICY "Users can view their own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
-- Note: A more complex policy is needed to allow viewing profiles during discovery, but we start simple.
CREATE POLICY "Users can update their own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- Function to handle new user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, first_name)
  VALUES (new.id, new.email, split_part(new.email, '@', 1));
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to create profile when auth.user is created
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();

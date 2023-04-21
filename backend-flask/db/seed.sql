-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Andrew Brown','andrew@exampro.co' , 'andrewbrown' ,'ce2f2bf5-e078-4c92-8d03-5a81bde76c5b'),
  ('Andrew Bayko','bayko@exampro.co' , 'bayko' ,'c21f2bf5-e078-4c92-8d03-5a81bde76c5b'),
  ('Uneku Ejiga','unekue2@gmail.com' , 'uneku' ,'ce1f2bf5-e078-4c92-8d03-5a81bde76c5b'),
  ('Londo Mollari', 'lmollari@centari.com','londo','ce1f2bf5-e078-4c92-8d03-5a81bde76c5s');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
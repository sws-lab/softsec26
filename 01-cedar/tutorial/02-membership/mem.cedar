permit(
  principal in Role::"vacationPhotoJudges",
  action == Action::"view",
  resource == Photo::"vacationPhoto94.jpg"
);

permit(
  principal in Role::"juniorPhotographerJudges",
  action == Action::"view",
  resource == Photo::"juniorPhotographerPhoto.jpg"
);

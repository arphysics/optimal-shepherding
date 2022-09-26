#bash

#ffmpeg -i concat:"./SI_videos_ODE/driving_2022_08_26_22_25/output_movie.mp4|./SI_videos_ODE/mustering_2022_08_26_22_14/output_movie.mp4" -codec copy output.mp4


ffmpeg -i concat:"./SI_videos_ODE/driving_2022_08_26_22_25/output_movie.mp4|./SI_videos_ODE/driving_2022_08_26_22_25/old_output_movie.mp4" -codec copy output.mp4



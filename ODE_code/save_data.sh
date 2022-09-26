
data=$(date +"%Y_%m_%d_%H_%M")
folder_name=$data
mkdir $folder_name
#echo $data


cp *.in $folder_name
cp data.out $folder_name
cp output_movie.mp4 $folder_name
cp *.png $folder_name
cp *.py $folder_name

mv $folder_name saved_data/

python3 ./get_data.py

year=`date +%Y `
month=`date +%m `
day=`date +%d `
hour=`date +%H`
now=$year-$month-$day-$hour


git config --global user.email ""
git config --global user.name "actioner"

git add .
git commit -m "$now"

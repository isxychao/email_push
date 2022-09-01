python -m pip install --upgrade pip
pip3 install -r requirements.txt

echo "Scraping data"
python3 ./get_data.py
echo "Scraping data Done"

year=`date +%Y `
month=`date +%m `
day=`date +%d `
hour=`date +%H`
now=$year-$month-$day-$hour

echo "Sending Email"
git config --global user.email "isxychao@outlook.com"
git config --global user.name "actioner"
echo "Sending Email Done"

echo "Pushing to github"
git add .
git commit -m "$now"
echo "Pushing to github Done"

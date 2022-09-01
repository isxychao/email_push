python -m pip install --upgrade pip
pip3 install -r requirements.txt

echo "Start scraping data"
python3 ./get_data.py
echo "Done"

year=`date +%Y `
month=`date +%m `
day=`date +%d `
hour=`date +%H`
now=$year-$month-$day-$hour

echo "Sending Email"
git config --global user.email "isxychao@outlook.com"
git config --global user.name "actioner"
echo "Done"

echo "Pushing to github"
git add .
git commit -m "$now"
echo "Done"

# set -e
#
for ((i = 27 ; i<29 ; i+=1))
  do
    for ((j = 1 ; j<5 ; j+=1))
      do python3 CND.py $i $j
    done
  done

# for ((i = 14 ; i>0 ; i-=2))
#   do python3 cloud.py 26 $i
# done
#
# python3 cloud.py 26 1


# python3 cloud.py 21 6

//fill a 2d array and return it

public class tony
{
    public static void main(String[] args)
    {
        int[][] array = new int[5][5];
        int count = 0;
        for(int i = 0; i < array.length; i++)
        {
            for(int j = 0; j < array[i].length; j++)
            {
                array[i][j] = count;
                count++;
            }
        }
        for(int i = 0; i < array.length; i++)
        {
            for(int j = 0; j < array[i].length; j++)
            {
                System.out.print(array[i][j] + " ");
            }
            System.out.println();
        }
    }

    //write a class method that takes a 2d array and returns average of all values
    public static double average(int[][] array)
    {
        double sum = 0;
        for(int i = 0; i < array.length; i++)
        {
            for(int j = 0; j < array[i].length; j++)
            {
                sum += array[i][j];
            }
        }
        return sum / (array.length * array[0].length);
    }
}
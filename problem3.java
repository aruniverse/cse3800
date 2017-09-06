import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class problem3 
{
	static double[] probabilities = new double[] { 0.45, 0.48, 0.5, 0.52, 0.55 };
	static int initial, goal, brokeCount, winCount;
	static String strategy;

	public static void main(String[] args) throws IOException
	{
		Scanner scan = new Scanner(System.in);
		System.out.println("Enter initial amount you have: ");
		initial = scan.nextInt();
		System.out.println("Enter how much you want to leave with: ");
		goal = scan.nextInt();
		System.out.println("Enter your strategy: ('timid' or 'bold') ");
		strategy = scan.next();
		scan.close();

		int i = initial, g = goal;	// used to reset the counters
		for(double d : probabilities)
		{	
			String outPath = strategy + "P_" + d + ".dat";		// file for final conclusion about the strategy for that p
			FileWriter fileWriter = new FileWriter(outPath);
			BufferedWriter bw = new BufferedWriter(fileWriter);	
			try
			{	
				System.out.println("Started writing to " + outPath);
				int avgNumBets = 0;
				for(int j=0; j<100; j++)	// 100 simulations for each probability
				{
					String outPath2 = strategy + "Out_" + d + ".dat";		// file for a simulation, there will be 100 simulations so this file will be overwritten 100x and the last simulations results will be held
					FileWriter fileWriter2 = new FileWriter(outPath2);
					BufferedWriter bw2 = new BufferedWriter(fileWriter2);		
					try 
					{
						System.out.println("Started writing to " + outPath2);
						String firstLine = "Iter: \t Initial: \t Goal: \t Broke: \t Won: \n";
						bw2.write(firstLine);
						int iter = 0;
						while(!checkIfBroke() && !checkIfWon())
						{
							String s = iter + "\t\t\t" + initial + "\t\t\t" + goal + "\t\t" + checkIfBroke() + "\t\t" + checkIfWon() + "\n";
							bw2.write(s);
							if(strategy.equals("timid"))
								timid(d);
							else
								bold(d);
							iter++;
						}
						String fin = iter + "\t\t\t" + initial + "\t\t\t" + goal + "\t\t" + checkIfBroke() + "\t\t" + checkIfWon() + "\n";
						bw2.write(fin);
						if(checkIfBroke())
							brokeCount++;
						else
							winCount++;
						bw2.close();
						avgNumBets+=iter;
					}
					catch (IOException e) 
					{
						System.out.println("Error writing to file " + outPath2);
					}
					initial = i;
					goal = g;
				}

				String info = strategy + "\n average num of bets = " + avgNumBets/100 + "\n num times you won = " + winCount + "\n num times you went broke = " + brokeCount;
				bw.write(info);
				bw.close();
				System.out.println("Done writing to " + outPath);
				avgNumBets = 0; brokeCount = 0; winCount = 0; // reset counters
			}
			catch (IOException e) 
			{
				System.out.println("Error writing to file " + outPath);
			}
		}
	}

	public static void timid(double d)
	{
		double random = Math.random();
		if (random<d)
			initial++;
		else
			initial--;
	}

	public static void bold(double d)
	{
		int k=0;
		if(goal>=2*initial)
			k = initial;
		else
			k = goal-initial;
		double random = Math.random();
		if(random<d) 
			initial+=k;
		else
			initial-=k;
	}

	public static boolean checkIfBroke()
	{
		return initial <= 0;
	}

	public static boolean checkIfWon()
	{
		return initial == goal;
	}

}
package automationTests;

import java.io.IOException;
import java.net.MalformedURLException;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.junit.internal.TextListener;
import org.junit.runner.JUnitCore;
import org.junit.runner.Result;

public class testSuite {
	static APIClient client;
	public static void main(String args[]) throws Exception {
		
		
		client = new APIClient("https://telecominfraproject.testrail.com");
		client.setUser("syama.devi@connectus.ai");
		client.setPassword("Connectus123$");

		JUnitCore junit = new JUnitCore();
		junit.addListener(new TextListener(System.out));
		Result result = junit.run(SystemTests.class);
		Result result1 = junit.run(ProfilesTest.class);
//		Result result2 = junit.run(NetworkTest.class);
		Result result3 = junit.run(LoginTest.class);
	    Result result4 = junit.run(AccountTest.class);
		Result result5 = junit.run(DashboardTest.class);
		if (result3.getFailureCount() > 0) {
			System.out.println("Tests failed.");
		    System.exit(1);
		    } else {
		    System.out.println("Tests finished successfully.");
		    System.exit(0);
		  }

		}
}

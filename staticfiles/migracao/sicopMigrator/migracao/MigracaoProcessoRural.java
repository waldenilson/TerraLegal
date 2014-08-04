package br.gov.incra.migracao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MigracaoProcessoRural {

	private String diretorio = "C://DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbprocessorural.sql";
	private String nomeArqLegado = "dump_tbprocesso.txt";
	
	public MigracaoProcessoRural()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoProcessoRural();
	}
		
	public String ler(String diretorio, String nomeArq)
	{
		
			File dir = new File( diretorio );
			File arq = new File(dir, nomeArq );
		 				
			try {
		        //Indicamos o arquivo que será lido
		        FileReader fileReader = new FileReader(arq);
		 
		        //Criamos o objeto bufferReader que nos
		        // oferece o método de leitura readLine()
		        BufferedReader bufferedReader =
		            new BufferedReader(fileReader);
		 
		        //String que irá receber cada linha do arquivo
		        String linha = "";
		        String conteudo = "";
		        String tabela = nomeArq.substring(5, nomeArq.length()-4);
	//	        System.out.println("table: "+tabela);
		        String leitura = "";
		        
		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O método readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1; int lixo = 0;
		        List<String> errosnumero = new ArrayList<String>();
		        List<String> erroscaixa = new ArrayList<String>();
		        List<String> errosgleba = new ArrayList<String>();
		        List<String> errosconjuge = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();

		        
//				LISTAS DAS COLUNAS
		        List<String> numero = new ArrayList<String>();
		        List<String> requerente = new ArrayList<String>();
		        List<String> cpfrequerente = new ArrayList<String>();
		        List<String> blconjuge = new ArrayList<String>();
		        List<String> cpfconjuge = new ArrayList<String>();
		        List<String> conjuge = new ArrayList<String>();
		        List<String> classificacao = new ArrayList<String>();

//		        System.out.println( "Proc: "+MigracaoAuxiliar.mapNomeConjuge() );
//    			System.exit(0);
//		        
		        while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split(";");
		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("\"", "");
		        		a = a.trim();
		        		
		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
		        			aux = "'"+a+"'";
	
		        		else if (a.startsWith("{") && a.endsWith("}") )
		        			aux = "'"+a+"'";
		        		
		        		else
		        		
		        			aux = "'"+a+"'";

		        		if(y==0) // numero
		        		{
		        			aux = (String) MigracaoAuxiliar.mapProcessoBase().get( a );
		        			if (aux == null)
		        				errosnumero.add("erro");
		        			numero.add(aux);
		        			String conj = (String) MigracaoAuxiliar.mapNomeConjuge().get( "'"+a.trim()+"'" );
		        			String cpfconj = (String) MigracaoAuxiliar.mapCPFConjuge().get( "'"+a.trim()+"'" );
		        			
		        			if(conj != null || cpfconj != null)
		        			{
		        				conjuge.add("'"+conj.replaceAll("'", "").trim()+"'");
		        				cpfconjuge.add("'"+cpfconj.replaceAll("'", "").trim()+"'");
		        			}
		        			else
		        			{
		        				conjuge.add("''");
		        				cpfconjuge.add("''");
		        			}		    
		        			
		        		}
		        		if(y==2) // requerente
		        		{
		        			requerente.add(aux);
		        		}

		        		if(y==3) // cpfrequerente
		        		{
		        			cpfrequerente.add(aux);
		        		}
		        		
		        		contaux += aux+"\t";
		        		
		        	}
//		        	cont = contaux.substring(0,contaux.length()-1);
		        			        	
		        	
//		        	System.out.println( cont );
	//	        	System.exit(0);
	//	        	cont = cont.replaceAll("\t", ",");
		        	
		        	x++;
	//	            System.out.println(conteudo);
		        }
		        for( int a=0; a<numero.size();a++)
	        	{
	        		int id = a+1;
	        		String cont = numero.get(a)+", "+requerente.get(a)+", "+cpfrequerente.get(a)+",false,null, "+cpfconjuge.get(a)+", "+conjuge.get(a);
		        	
	 //        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
//	        		cont = cont.replaceAll("''", "null");
	        		tabela = "tbprocessorural";
	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();

		        System.out.println("ERROS NUMERO: "+errosnumero.size()+
		        		"\nERROS REQUERENTE: "+erroscaixa.size()+
		        		"\nERROS CPFREQUERENTE: "+errosgleba.size()+
		        		"\nERROS CONJUGE: "+errosconjuge.size()+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size()+"\n\n\n");

		        System.out.println("numero: "+numero.size()+
		        		"\nREQUERENTE: "+requerente.size()+
		        		"\nCPFREQUERENTE: "+cpfrequerente.size()+
		        		"\n\n\n");
		        
		        return conteudo;
		    } catch (IOException e) {
		        e.printStackTrace();
		        return null;
		    }

	}
	
	// método para escrever no TXT  
    public void escreve (String conteudo, File arq){  
          
        try {  
            FileWriter escreve = new FileWriter(arq, true);  
            conteudo += System.getProperty("line.separator"); // pular linha  
            escreve.write(conteudo); // escrever o conteúdo  
            escreve.close();  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
		
}

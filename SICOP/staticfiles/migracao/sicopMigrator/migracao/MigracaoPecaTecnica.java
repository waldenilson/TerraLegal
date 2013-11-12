package br.gov.incra.migracao;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class MigracaoPecaTecnica {

	private String diretorio = "c:\\DEVELOPER/SICOP/Migracao";
	private String nomeArqMigracao = "scriptTbpecastecnica.sql";
	private String nomeArqLegado = "dump_tbpecastecnicas.txt";
	
	public MigracaoPecaTecnica()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new MigracaoPecaTecnica();
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
		        List<String> erroscontrato= new ArrayList<String>();
		        List<String> erroscaixa = new ArrayList<String>();
		        List<String> errosgleba = new ArrayList<String>();
		        List<String> perfeita = new ArrayList<String>();
		        
		        while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split(";");
		        	
		        	if(s.length != 13)
		        		perfeita.add("ok");
		        	
		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("\"", "");
		        		a = a.trim();
		        		
		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
		        			aux = "'"+a+"'";
	
		        		else if (a.startsWith("{") && a.endsWith("}") )
		        		{
		        			a = a.replaceAll("\\{", "");
			        		a = a.replaceAll("}", "");
		        			aux = "'"+a+"'";
			        	}
		        		else
		        			aux = "'"+a+"'";
		        		
		        		
		        		if(y==1) // contrato
		        		{
		        			aux = (String) MigracaoAuxiliar.mapContrato().get( a );
		        			if (aux == null)
		        				erroscontrato.add("erro-contrato | "+a);
		        		}
		        		else if(y==5 || y==6 || y==7) // booleanos
		        		{
		        			if (a == null || a.equals("nao") || a.equals("pen") || a.equals("rej"))
		        				aux = "false";
		        			else if (a.equals("sim"))
		        				aux = "true";
		        		}
		        		else if(y==8) // obs
		        		{
		        			if(a.isEmpty())
//		        				System.out.println("OBSERVACAO: "+aux);
		        				aux = "'nenhuma observacao'"; 
		        		}
		        		else if(y==9) // caixa (pastageo)
		        		{
		        			aux = (String) MigracaoAuxiliar.mapCaixa().get( a );
		        			if (aux == null)
		        				erroscaixa.add("erro-caixa | "+a);
		        		}
		        		
		        		// verificar area e perimetro
		        		else if(y==10 && y==11) 
		        		{
		        			if (a.isEmpty())
		        				aux = "0";
		        		}
		        		
		        		else if(y==12) // gleba
		        		{
		        			if(a.isEmpty() || a.equals("-"))
		        				a = "DADOS MIGRADOS GLEBA";
		        			aux = (String) MigracaoAuxiliar.mapGleba().get( a.toUpperCase() );
		        			if (aux == null)
		        			{
		        				aux = (String) MigracaoAuxiliar.mapGleba().get( "DADOS MIGRADOS GLEBA".toUpperCase() );
			        			errosgleba.add("erro | "+a);
		        			}
		        		}
		        		
		        		// verificar sem cpf
		        		else if(y==3) 
		        		{
		        			if (a.isEmpty())
		        				aux = "'nonecpf'";
		        		}
		        		// verificar sem rquerente
		        		else if(y==4) 
		        		{
		        			if (a.isEmpty())
		        				aux = "'nonerequerente'";
		        		}
		        		
		        		// verificar observacoes
		        		else if(y==8) 
		        		{
		        			aux = a.replaceAll("\t", " ");
		        			aux = aux.replaceAll("\n", " ");
		        		}
		        				
		        		contaux += aux+"\t";
		        		
		        	}
		        	cont = contaux.substring(0,contaux.length()-1);
		        	
		        	
		        	
	//        		cont = cont.replaceAll("\t\t", "\t");
	        		cont = cont.replaceAll("\t", ",");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll(",,", ",null,");
	        		cont = cont.replaceAll("''", "null");
		        	
//		        	System.out.println( cont );
	//	        	System.exit(0);
	//	        	cont = cont.replaceAll("\t", ",");
	        		
	        		if(cont.contains("'nonecpf'") && cont.contains("'nonerequerente'"))
	        		{
	        			// lixo
	        			lixo++;
	        		}
	        		else
	        		{
			        	cont += ", 1,"+x;
			        	tabela = "tbpecastecnicas";
			        	conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
			        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
			        	x++;
	        		}
	//	            System.out.println(conteudo);
		        }
		        System.out.println("conteudo: "+leitura);
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();
		        
		        System.out.println("ERROS CONTRATO: "+erroscontrato+
		        		"\nERROS CAIXA: "+erroscaixa+
		        		"\nERROS GLEBA: "+errosgleba+
		        		"\nREGISTROS: "+x+
		        		"\nLIXOS: "+lixo+
		        		"\nREGISTROS PERFEITOS: "+perfeita.size());
		        
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

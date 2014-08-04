package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class IntegracaoSisterleg {

	private String diretorio = "c:\\DEVELOPER/SICOP/Migracao/Report/";
	private String nomeArqMigracao = "scriptIntegracao.sql";
	private String nomeArqLegado = "pendencias-getat-10-32.csv";
	
	public IntegracaoSisterleg()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new IntegracaoSisterleg();
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
		        String tabela = "integracao";//nomeArq.substring(5, nomeArq.length()-4);
	//	        System.out.println("table: "+tabela);
		        String leitura = "";
		        
		        
//				LISTAS DAS COLUNAS
		        List<String> processo = new ArrayList<String>();
		        List<String> nome = new ArrayList<String>();
		        List<String> cpf = new ArrayList<String>();
		        List<String> caixa = new ArrayList<String>();
		        List<String> endereco = new ArrayList<String>();
		        List<String> telefone = new ArrayList<String>();
		        List<String> conjuge = new ArrayList<String>();
		        List<String> apelido = new ArrayList<String>();

		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O método readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1;
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
		        		
		        		
		        		if(y==0)
		        			processo.add(aux);
		        		if(y==3)
		        			nome.add(aux);
		        		if(y==5)
		        			cpf.add(aux);
		        		
		        	}
		        }
		        
		        for( int a=0; a<processo.size();a++)
	        	{
		        	
		        		String cont = processo.get(a)+", "+nome.get(a)+", "+cpf.get(a)+", '', '', '', '', 'pendencias getat 10'";
			        	
		 //        		cont = cont.replaceAll("\t\t", "\t");
		        		cont = cont.replaceAll("\t", ",");
		        		cont = cont.replaceAll(",,", ",null,");
		        		cont = cont.replaceAll(",,", ",null,");
		        		cont = cont.replaceAll("''", "null");
		        		tabela = "integracao";
 	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
			        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	
		        }

		        
		        System.out.println("conteudo: "+processo.size());
		        
	//	        escreve(conteudo, new File(dir, "dump_"+tabela+"_db.sql") );
		 
		        //liberamos o fluxo dos objetos
		        // ou fechamos o arquivo
		        fileReader.close();
		        bufferedReader.close();
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

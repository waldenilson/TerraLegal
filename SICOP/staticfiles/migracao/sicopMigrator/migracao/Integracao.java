package br.gov.incra.migracao;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Integracao {

	private String diretorio = "c:\\DEVELOPER/SICOP/Migracao/Report/";
	private String nomeArqMigracao = "scriptIntegracao.sql";
	private String nomeArqLegado = "integracao.txt";
	
	public Integracao()
	{		
		File dir = new File( diretorio );
		String todosScripts = "";
			String conteudo = ler(diretorio, nomeArqLegado);
			todosScripts += conteudo;
		escreve(todosScripts, new File(dir, nomeArqMigracao) );
	}
	
	public static void main(String a[])
	{
		new Integracao();
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
		        List<String> municipio = new ArrayList<String>();
		        List<String> conjuge = new ArrayList<String>();
		        List<String> apelido = new ArrayList<String>();
		        List<String> cpflerro = new ArrayList<String>();

		        
		        
		        //Fazemos um loop linha a linha no arquivo,
		        // enquanto ele seja diferente de null.
		        //O método readLine() devolve a linha na
		        // posicao do loop para a variavel linha.
		        int x = 1;
		        int cpferro = 0;
	        	while ( ( linha = bufferedReader.readLine() ) != null) {
		            
		        	//Aqui imprimimos a linha
	//	        	tabela = "tbconjuge";
		        	
	//	        	String cont = linha.replaceAll("\t", ",");
		        	String cont = linha;
		        	String contaux = "";
		        	String[] s = cont.split("\t");
		        	for(int y=0; y < s.length ; y++)
		        	{
		        		String aux = "";
		        		String a = s[y];
		        		
		        		a = a.replaceAll("\"", "");
//		        		a = a.trim();
		        		
//		        		if (a.startsWith("20") && a.contains("-") && a.contains(":"))
//		        			aux = "'"+a+"'";
//	
//		        		else if (a.startsWith("{") && a.endsWith("}") )
//		        			aux = "'"+a+"'";
//		        		
//		        		else
//		        		
//		        			aux = "'"+a+"'";		        		
	
		        		aux = a;
		        		
		        		if(y==0)
		        			processo.add(aux);
		        		if(y==1)
		        		{
		        			nome.add( new String(aux.getBytes(), "UTF-8") );
		        		}
		        		if(y==2)
		        		{
		        			if(aux.startsWith("0"))
		        				aux = aux.substring(1, aux.length());
		        			cpf.add(aux);
		        			if(aux.length() < 11 )
		        			{
		        				cpferro++;
		        				cpflerro.add(aux);
		        			}
		        		}
		        		if(y==3)
		        		{
		        			String nom = cpf.get( endereco.size() );
		        			nom = nom.replaceAll("'", "");
//		        			System.out.println(":"+proc+":");
		        			aux = (String) MigracaoAuxiliar.mapSisterlegPlanilhaApelido().get( nom );
		        			apelido.add( aux );
		        		}
		        		if(y==3)
		        		{
		        			String nom = cpf.get( municipio.size() );
		        			nom = nom.replaceAll("'", "");
//		        			System.out.println(":"+proc+":");
		        			aux = (String) MigracaoAuxiliar.mapSisterlegPlanilhaMunicipio().get( nom );		        		
		        			municipio.add(aux);
		        		}
		        		if(y==4)
		        		{
		        			String nom = cpf.get( conjuge.size() );
		        			nom = nom.replaceAll("'", "");
//		        			System.out.println(":"+proc+":");
		        			aux = (String) MigracaoAuxiliar.mapSisterlegPlanilhaConjuge().get( nom );		        			
		        			conjuge.add( aux );
		        		}
		        		if(y==5)
		        		{
		        			String nom = cpf.get( endereco.size() );
		        			nom = nom.replaceAll("'", "");
//		        			System.out.println(":"+proc+":");
		        			aux = (String) MigracaoAuxiliar.mapSisterlegPlanilhaEndereco().get( nom );
		        			if(aux != null)
		        				endereco.add( new String(aux.getBytes(), "ISO-8859-1") );
		        			else
		        				endereco.add( aux );
		        		}
		        		if(y==6)
		        		{
		        			String nom = cpf.get( telefone.size() );
		        			nom = nom.replaceAll("'", "");
//		        			System.out.println(":"+proc+":");
		        			aux = (String) MigracaoAuxiliar.mapSisterlegPlanilhaTelefone().get( nom );		        		
		        			telefone.add(aux);
		        		}
		        		if(y==7)
		        			caixa.add(aux);	        		
		        	}
		        }
		        
		        for( int a=0; a<processo.size();a++)
	        	{
		        	
		        		String cont = "'"+processo.get(a)+"', '"+ nome.get(a)+"', '"+cpf.get(a)+
		        				"', '"+apelido.get(a)+
		        				"', '"+conjuge.get(a)+"', '"+endereco.get(a)+
		        				"', '"+telefone.get(a)+"', '"+
		        		caixa.get(a).toUpperCase()+"'";
			        	
		 //        		cont = cont.replaceAll("\t\t", "\t");
		        		cont = cont.replaceAll("\t", ",");
		        		cont = cont.replaceAll(",,", ",null,");
		        		cont = cont.replaceAll(",,", ",null,");
//		        		cont = cont.replaceAll("''", "null");
		        		cont = cont.replaceAll("null", "");
		        		tabela = "integracao";
 	        		conteudo += "INSERT INTO "+tabela+" values( "+cont+" );\n";
			        	leitura += x+"\t"+"INSERT INTO "+tabela+" values( "+cont+" );\n";
		        	
		        }
		        
		        System.out.println("conteudo: "+leitura);
		        System.out.println("erros cpf: "+cpferro);
		        System.out.println("erros cpf: "+cpflerro);
		        
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